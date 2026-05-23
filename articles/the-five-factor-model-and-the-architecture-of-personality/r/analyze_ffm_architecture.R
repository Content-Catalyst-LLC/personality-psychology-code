args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_ffm_architecture.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_ffm_items.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

domains <- c("extraversion_score", "agreeableness_score", "conscientiousness_score", "neuroticism_score", "openness_score")
facets <- c("sociability_score", "assertiveness_score", "compassion_score", "politeness_score", "orderliness_score", "industriousness_score", "anxiety_score", "volatility_score", "aesthetics_score", "intellect_score")
outcomes <- c("outcome_score", "broad_life_functioning", "relationship_functioning", "creative_engagement", "emotional_distress")
derived <- c("facet_profile_dispersion", "hierarchy_consistency_index", "bandwidth_fidelity_gap", "domain_facet_alignment")

alpha_score <- function(df) {
  k <- ncol(df)
  item_vars <- apply(df, 2, var)
  total_var <- var(rowSums(df))
  (k / (k - 1)) * (1 - sum(item_vars) / total_var)
}

data$conscientiousness_rescored <- rowMeans(data[, c("c1", "c2", "c3", "c4", "c5", "c6")])
data$orderliness_rescored <- rowMeans(data[, c("o1", "o2", "o3")])
data$industriousness_rescored <- rowMeans(data[, c("i1", "i2", "i3")])

reliability <- data.frame(
  scale = c("full_item_pool_item1_item60", "conscientiousness_c1_c6", "orderliness_o1_o3", "industriousness_i1_i3"),
  level = c("broad_item_pool", "domain_item_set", "facet_item_set", "facet_item_set"),
  n_items = c(60, 6, 3, 3),
  cronbach_alpha = c(
    alpha_score(data[, paste0("item", 1:60)]),
    alpha_score(data[, c("c1", "c2", "c3", "c4", "c5", "c6")]),
    alpha_score(data[, c("o1", "o2", "o3")]),
    alpha_score(data[, c("i1", "i2", "i3")])
  )
)

models <- list(
  broad_life_functioning_from_domains = lm(broad_life_functioning ~ extraversion_score + agreeableness_score + conscientiousness_score + neuroticism_score + openness_score, data = data),
  relationship_functioning_from_social_domains = lm(relationship_functioning ~ extraversion_score + agreeableness_score + sociability_score + compassion_score, data = data),
  creative_engagement_from_openness = lm(creative_engagement ~ openness_score + aesthetics_score + intellect_score, data = data),
  emotional_distress_from_neuroticism = lm(emotional_distress ~ neuroticism_score + anxiety_score + volatility_score, data = data),
  outcome_from_conscientiousness_domain = lm(outcome_score ~ conscientiousness_score, data = data),
  outcome_from_conscientiousness_facets = lm(outcome_score ~ orderliness_score + industriousness_score, data = data),
  facet_to_domain_hierarchy = lm(conscientiousness_score ~ orderliness_score + industriousness_score, data = data)
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

delta_r2 <- data.frame(
  comparison = c("facet_minus_domain_prediction_r2_for_outcome_score", "hierarchy_model_r2_conscientiousness_from_facets"),
  delta_r2 = c(
    summary(models$outcome_from_conscientiousness_facets)$r.squared - summary(models$outcome_from_conscientiousness_domain)$r.squared,
    summary(models$facet_to_domain_hierarchy)$r.squared
  )
)

write.csv(summary(data[, c(domains, outcomes, derived)]), file.path(outputs, "r_domain_summary.csv"))
write.csv(summary(data[, c(facets, outcomes, derived)]), file.path(outputs, "r_facet_summary.csv"))
write.csv(cor(data[, c(domains, facets, outcomes, derived)], use = "pairwise.complete.obs"), file.path(outputs, "r_ffm_correlations.csv"))
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(delta_r2, file.path(outputs, "r_domain_facet_comparison.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_ffm_items.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
