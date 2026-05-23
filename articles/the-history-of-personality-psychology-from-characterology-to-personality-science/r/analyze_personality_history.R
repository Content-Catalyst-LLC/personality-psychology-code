args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_personality_history.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_personality_history_items.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

items <- paste0("item", 1:60)
c_items <- paste0("c", 1:6)
traits <- c("extraversion_score", "agreeableness_score", "conscientiousness_score", "neuroticism_score", "openness_score")
history <- c("characterology_typology_index", "psychometric_structure_index", "person_situation_index", "narrative_identity_index", "measurement_invariance_caution_index", "historical_method_maturity_index")

alpha_score <- function(df) {
  k <- ncol(df)
  item_vars <- apply(df, 2, var)
  total_var <- var(rowSums(df))
  (k / (k - 1)) * (1 - sum(item_vars) / total_var)
}

data$conscientiousness_rescored <- rowMeans(data[, c_items])
data$stability_change <- data$conscientiousness_t2 - data$conscientiousness_t1

reliability <- data.frame(
  scale = c("conscientiousness_c1_c6", "full_personality_item_pool_item1_item60"),
  level = c("short_trait_scale", "broad_item_pool"),
  n_items = c(6, 60),
  cronbach_alpha = c(alpha_score(data[, c_items]), alpha_score(data[, items]))
)

# PCA using base R.
scaled_items <- scale(data[, items])
pca <- prcomp(scaled_items, center = FALSE, scale. = FALSE)
component_scores <- as.data.frame(pca$x[, 1:10])
names(component_scores) <- paste0("component_", 1:10)
data <- cbind(data, component_scores)

pca_summary <- data.frame(
  component = 1:10,
  explained_variance_ratio = (pca$sdev[1:10]^2) / sum(pca$sdev^2),
  cumulative_explained_variance = cumsum((pca$sdev[1:10]^2) / sum(pca$sdev^2))
)

data$person_situation_interaction <- data$trait_score * data$situation_strength

models <- list(
  conscientiousness_stability_t2_from_t1 = lm(conscientiousness_t2 ~ conscientiousness_t1, data = data),
  behavior_from_trait_situation_interaction = lm(behavior_score ~ trait_score + situation_strength + person_situation_interaction, data = data),
  psychometric_structure_from_traits = lm(psychometric_structure_index ~ extraversion_score + agreeableness_score + conscientiousness_score + neuroticism_score + openness_score, data = data),
  historical_method_maturity = lm(historical_method_maturity_index ~ psychometric_structure_index + person_situation_index + narrative_identity_index + measurement_invariance_caution_index, data = data),
  typology_residual = lm(characterology_typology_index ~ psychometric_structure_index + historical_method_maturity_index, data = data)
)

model_fit <- data.frame(
  model = names(models),
  r_squared = sapply(models, function(m) summary(m)$r.squared),
  adj_r_squared = sapply(models, function(m) summary(m)$adj.r.squared),
  n = nrow(data)
)

coef_table <- function(model, model_name) {
  coefs <- summary(model)$coefficients
  data.frame(model = model_name, term = rownames(coefs), estimate = coefs[,1], standard_error = coefs[,2], t_value = coefs[,3], p_value = coefs[,4], row.names = NULL)
}

model_coefficients <- do.call(rbind, Map(coef_table, models, names(models)))

stability_summary <- data.frame(
  measure = "conscientiousness_rank_order_stability",
  correlation = cor(data$conscientiousness_t1, data$conscientiousness_t2),
  mean_t1 = mean(data$conscientiousness_t1),
  mean_t2 = mean(data$conscientiousness_t2),
  mean_change = mean(data$stability_change),
  sd_change = sd(data$stability_change)
)

write.csv(summary(data[, c(traits, "conscientiousness_t1", "conscientiousness_t2", "behavior_score", "trait_score", "situation_strength")]), file.path(outputs, "r_trait_summary.csv"))
write.csv(summary(data[, c(history, "stability_change")]), file.path(outputs, "r_history_index_summary.csv"))
write.csv(cor(data[, c(traits, history, "conscientiousness_t1", "conscientiousness_t2", "behavior_score", "trait_score", "situation_strength")], use = "pairwise.complete.obs"), file.path(outputs, "r_personality_history_correlations.csv"))
write.csv(pca_summary, file.path(outputs, "r_pca_dimensionality_summary.csv"), row.names = FALSE)
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(stability_summary, file.path(outputs, "r_stability_summary.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_personality_history_items.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
