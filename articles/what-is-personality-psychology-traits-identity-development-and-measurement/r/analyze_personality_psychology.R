args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_personality_psychology.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
personality_path <- file.path(root, "data", "synthetic_personality_items.csv")
state_path <- file.path(root, "data", "synthetic_person_situation_observations.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(personality_path, stringsAsFactors = FALSE)
state_data <- read.csv(state_path, stringsAsFactors = FALSE)

items <- paste0("item", 1:60)
traits <- c("conscientiousness_score", "extraversion_score", "neuroticism_score")
outcomes <- c("identity_coherence", "life_satisfaction", "social_functioning", "developmental_integration")
indices <- c("measurement_reliability_index", "identity_trait_alignment_index", "person_situation_sensitivity_index", "responsible_interpretation_index")

alpha_score <- function(df) {
  k <- ncol(df)
  item_vars <- apply(df, 2, var)
  total_var <- var(rowSums(df))
  (k / (k - 1)) * (1 - sum(item_vars) / total_var)
}

data$conscientiousness_rescored <- rowMeans(data[, paste0("c", 1:6)])
data$extraversion_rescored <- rowMeans(data[, paste0("e", 1:6)])
data$neuroticism_rescored <- rowMeans(data[, paste0("n", 1:6)])

reliability <- data.frame(
  scale = c("conscientiousness", "extraversion", "neuroticism", "full_personality_item_pool_item1_item60"),
  n_items = c(6, 6, 6, 60),
  cronbach_alpha = c(
    alpha_score(data[, paste0("c", 1:6)]),
    alpha_score(data[, paste0("e", 1:6)]),
    alpha_score(data[, paste0("n", 1:6)]),
    alpha_score(data[, items])
  )
)

scaled_items <- scale(data[, items])
pca <- prcomp(scaled_items, center = FALSE, scale. = FALSE)
component_scores <- as.data.frame(pca$x[, 1:10])
names(component_scores) <- paste0("personality_component_", 1:10)
data <- cbind(data, component_scores)

pca_summary <- data.frame(
  component = 1:10,
  explained_variance_ratio = (pca$sdev[1:10]^2) / sum(pca$sdev^2),
  cumulative_explained_variance = cumsum((pca$sdev[1:10]^2) / sum(pca$sdev^2))
)

state_data$trait_x_situation <- state_data$trait_score * state_data$situation_strength

models <- list(
  identity_coherence_from_traits = lm(identity_coherence ~ conscientiousness_score + extraversion_score + neuroticism_score, data = data),
  life_satisfaction_from_traits = lm(life_satisfaction ~ conscientiousness_score + extraversion_score + neuroticism_score, data = data),
  social_functioning_from_traits = lm(social_functioning ~ conscientiousness_score + extraversion_score + neuroticism_score, data = data),
  developmental_integration_from_traits_and_identity = lm(developmental_integration ~ conscientiousness_score + extraversion_score + neuroticism_score + identity_coherence, data = data),
  responsible_interpretation_from_indices = lm(responsible_interpretation_index ~ measurement_reliability_index + identity_trait_alignment_index + person_situation_sensitivity_index, data = data),
  person_situation_behavior_model = lm(behavior_score ~ trait_score + situation_strength + trait_x_situation + observed_regulation + contextual_constraint, data = state_data)
)

model_fit <- data.frame(
  model = names(models),
  r_squared = sapply(models, function(m) summary(m)$r.squared),
  adj_r_squared = sapply(models, function(m) summary(m)$adj.r.squared),
  n = sapply(models, function(m) nobs(m))
)

coef_table <- function(model, model_name) {
  coefs <- summary(model)$coefficients
  data.frame(model = model_name, term = rownames(coefs), estimate = coefs[,1], standard_error = coefs[,2], t_value = coefs[,3], p_value = coefs[,4], row.names = NULL)
}

model_coefficients <- do.call(rbind, Map(coef_table, models, names(models)))

person_state_summary <- aggregate(
  cbind(behavior_score, trait_score, situation_strength, trait_x_situation, observed_regulation, contextual_constraint) ~ person_id,
  data = state_data,
  FUN = mean
)

write.csv(summary(data[, c(traits, outcomes, indices)]), file.path(outputs, "r_trait_outcome_summary.csv"))
write.csv(cor(data[, c(traits, outcomes, indices)], use = "pairwise.complete.obs"), file.path(outputs, "r_trait_outcome_correlations.csv"))
write.csv(pca_summary, file.path(outputs, "r_pca_dimensionality_summary.csv"), row.names = FALSE)
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(person_state_summary, file.path(outputs, "r_person_situation_summary.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_personality_items.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
