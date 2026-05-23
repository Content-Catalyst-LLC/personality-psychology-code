args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_temperament_personality.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_temperament_personality_longitudinal.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)
temperament <- c("inhibition_t1", "negative_affect_t1", "surgency_t1", "effortful_control_t1")
environment <- c("parenting_support_t1", "family_stress_t1", "classroom_support_t2", "peer_support_t2", "institutional_stability_t2")
outcomes <- c("conscientiousness_t2", "neuroticism_t2", "social_confidence_t2", "regulation_skill_t2")
derived <- c("reactivity_regulation_balance", "environmental_support_index", "developmental_risk_index", "adaptive_pathway_score")

context_summary <- aggregate(data[, c(temperament, environment, outcomes, derived)], by = list(developmental_context = data$developmental_context), FUN = mean)
correlations <- cor(data[, c(temperament, environment, outcomes, derived)], use = "pairwise.complete.obs")

models <- list(
  conscientiousness_t2 = lm(conscientiousness_t2 ~ effortful_control_t1 + parenting_support_t1 + family_stress_t1 + classroom_support_t2, data = data),
  neuroticism_t2 = lm(neuroticism_t2 ~ inhibition_t1 * parenting_support_t1 + negative_affect_t1 + family_stress_t1, data = data),
  social_confidence_t2 = lm(social_confidence_t2 ~ inhibition_t1 + surgency_t1 + classroom_support_t2 + peer_support_t2 + family_stress_t1, data = data),
  regulation_skill_t2 = lm(regulation_skill_t2 ~ effortful_control_t1 * classroom_support_t2 + parenting_support_t1 + family_stress_t1, data = data),
  developmental_risk_index = lm(developmental_risk_index ~ reactivity_regulation_balance * family_stress_t1 + environmental_support_index, data = data),
  adaptive_pathway_score = lm(adaptive_pathway_score ~ effortful_control_t1 + environmental_support_index + family_stress_t1 + reactivity_regulation_balance, data = data)
)

model_fit <- data.frame(model = names(models), r_squared = sapply(models, function(m) summary(m)$r.squared), n = nrow(data))

coef_table <- function(model, model_name) {
  coefs <- summary(model)$coefficients
  data.frame(model = model_name, term = rownames(coefs), estimate = coefs[,1], standard_error = coefs[,2], t_value = coefs[,3], p_value = coefs[,4], row.names = NULL)
}

model_coefficients <- do.call(rbind, Map(coef_table, models, names(models)))

write.csv(context_summary, file.path(outputs, "r_context_summary.csv"), row.names = FALSE)
write.csv(correlations, file.path(outputs, "r_temperament_personality_correlations.csv"))
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_temperament_personality_longitudinal.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
