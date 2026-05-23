args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_trait_stability.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
trait_path <- file.path(root, "data", "synthetic_trait_items.csv")
state_path <- file.path(root, "data", "synthetic_state_observations.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

trait_data <- read.csv(trait_path, stringsAsFactors = FALSE)
state_data <- read.csv(state_path, stringsAsFactors = FALSE)

alpha_score <- function(df) {
  k <- ncol(df)
  item_vars <- apply(df, 2, var)
  total_var <- var(rowSums(df))
  (k / (k - 1)) * (1 - sum(item_vars) / total_var)
}

reliability <- data.frame(
  scale = c("conscientiousness", "extraversion", "neuroticism"),
  n_items = c(6, 6, 6),
  cronbach_alpha = c(
    alpha_score(trait_data[, paste0("c", 1:6)]),
    alpha_score(trait_data[, paste0("e", 1:6)]),
    alpha_score(trait_data[, paste0("n", 1:6)])
  )
)

trait_data$conscientiousness_rescored <- rowMeans(trait_data[, paste0("c", 1:6)])
trait_data$extraversion_rescored <- rowMeans(trait_data[, paste0("e", 1:6)])
trait_data$neuroticism_rescored <- rowMeans(trait_data[, paste0("n", 1:6)])

person_means <- aggregate(
  cbind(state_conscientiousness, state_extraversion, state_neuroticism, situational_activation, situational_constraint) ~ person_id,
  data = state_data,
  FUN = mean
)
names(person_means) <- c("person_id", "mean_state_conscientiousness", "mean_state_extraversion", "mean_state_neuroticism", "mean_situational_activation", "mean_situational_constraint")

person_sds <- aggregate(
  cbind(state_conscientiousness, state_extraversion, state_neuroticism) ~ person_id,
  data = state_data,
  FUN = sd
)
names(person_sds) <- c("person_id", "sd_state_conscientiousness", "sd_state_extraversion", "sd_state_neuroticism")

person_counts <- aggregate(occasion ~ person_id, data = state_data, FUN = length)
names(person_counts) <- c("person_id", "n_observations")

person_summary <- merge(merge(person_means, person_sds, by = "person_id"), person_counts, by = "person_id")
merged <- merge(trait_data, person_summary, by = "person_id")

merged$trait_state_alignment_index <- pmax(0, pmin(10, 10 - (
  abs(merged$conscientiousness_score - merged$mean_state_conscientiousness) +
  abs(merged$extraversion_score - merged$mean_state_extraversion) +
  abs(merged$neuroticism_score - merged$mean_state_neuroticism)
)))
merged$state_variability_index <- pmax(0, pmin(10,
  merged$sd_state_conscientiousness + merged$sd_state_extraversion + merged$sd_state_neuroticism
))
merged$person_situation_sensitivity_index <- pmax(0, pmin(10,
  merged$mean_situational_activation * 0.45 +
  merged$mean_situational_constraint * 0.35 +
  merged$state_variability_index * 0.20
))
merged$aggregation_reliability_index <- pmax(0, pmin(10,
  sqrt(merged$n_observations) * 1.15 +
  merged$trait_state_alignment_index * 0.35 -
  merged$state_variability_index * 0.18
))

models <- list(
  mean_state_conscientiousness_from_trait = lm(mean_state_conscientiousness ~ conscientiousness_score, data = merged),
  mean_state_extraversion_from_trait = lm(mean_state_extraversion ~ extraversion_score, data = merged),
  mean_state_neuroticism_from_trait = lm(mean_state_neuroticism ~ neuroticism_score, data = merged),
  trait_state_alignment_from_variability = lm(trait_state_alignment_index ~ state_variability_index + person_situation_sensitivity_index + aggregation_reliability_index, data = merged)
)

model_fit <- data.frame(
  model = names(models),
  r_squared = sapply(models, function(m) summary(m)$r.squared),
  adj_r_squared = sapply(models, function(m) summary(m)$adj.r.squared),
  n = nrow(merged)
)

coef_table <- function(model, model_name) {
  coefs <- summary(model)$coefficients
  data.frame(model = model_name, term = rownames(coefs), estimate = coefs[,1], standard_error = coefs[,2], t_value = coefs[,3], p_value = coefs[,4], row.names = NULL)
}

model_coefficients <- do.call(rbind, Map(coef_table, models, names(models)))

variance_components <- do.call(rbind, lapply(c("state_conscientiousness", "state_extraversion", "state_neuroticism"), function(v) {
  means <- aggregate(as.formula(paste(v, "~ person_id")), data = state_data, FUN = mean)[,2]
  vars <- aggregate(as.formula(paste(v, "~ person_id")), data = state_data, FUN = var)[,2]
  between <- var(means)
  within <- mean(vars, na.rm = TRUE)
  total <- between + within
  data.frame(
    state_variable = v,
    between_person_variance = between,
    within_person_variance = within,
    between_person_share = between / total,
    within_person_share = within / total
  )
}))

write.csv(summary(trait_data[, c("conscientiousness_score", "extraversion_score", "neuroticism_score")]), file.path(outputs, "r_trait_summary.csv"))
write.csv(summary(state_data[, c("state_conscientiousness", "state_extraversion", "state_neuroticism", "situational_activation", "situational_constraint")]), file.path(outputs, "r_state_summary.csv"))
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(cor(merged[, c("conscientiousness_score", "mean_state_conscientiousness", "extraversion_score", "mean_state_extraversion", "neuroticism_score", "mean_state_neuroticism", "trait_state_alignment_index", "state_variability_index")], use = "pairwise.complete.obs"), file.path(outputs, "r_trait_state_correlations.csv"))
write.csv(variance_components, file.path(outputs, "r_variance_components.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(merged, file.path(outputs, "r_trait_state_merged.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
