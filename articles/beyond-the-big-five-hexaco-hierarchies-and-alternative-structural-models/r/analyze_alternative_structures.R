args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_alternative_structures.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_alternative_structure_items.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

bf <- c("bf_extraversion", "bf_agreeableness", "bf_conscientiousness", "bf_neuroticism", "bf_openness")
hx <- c("hx_honesty_humility", "hx_emotionality", "hx_extraversion", "hx_agreeableness", "hx_conscientiousness", "hx_openness")
facets <- c("sincerity_facet", "fairness_facet", "greed_avoidance_facet", "modesty_facet", "patience_facet", "forgiveness_facet", "anxiety_facet", "sentimentality_facet")
outcomes <- c("outcome_integrity", "outcome_interpersonal_trust", "outcome_broad_functioning", "outcome_exploitative_risk")
derived <- c("hexaco_increment_marker", "repartitioning_gap", "structural_comparison_index", "facet_granularity_index")
items <- paste0("item", 1:72)

alpha_score <- function(df) {
  k <- ncol(df)
  item_vars <- apply(df, 2, var)
  total_var <- var(rowSums(df))
  (k / (k - 1)) * (1 - sum(item_vars) / total_var)
}

reliability <- data.frame(
  scale = c("big_five_proxy_items_1_60", "hexaco_proxy_items_1_72", "honesty_humility_facets", "emotionality_agreeableness_repartition"),
  level = c("five_factor_proxy_pool", "six_factor_proxy_pool", "hexaco_domain_facets", "repartitioning_facets"),
  n_items = c(60, 72, 4, 4),
  cronbach_alpha = c(
    alpha_score(data[, paste0("item", 1:60)]),
    alpha_score(data[, items]),
    alpha_score(data[, c("sincerity_facet", "fairness_facet", "greed_avoidance_facet", "modesty_facet")]),
    alpha_score(data[, c("patience_facet", "forgiveness_facet", "anxiety_facet", "sentimentality_facet")])
  )
)

models <- list(
  integrity_from_big_five = lm(outcome_integrity ~ bf_extraversion + bf_agreeableness + bf_conscientiousness + bf_neuroticism + bf_openness, data = data),
  integrity_from_hexaco = lm(outcome_integrity ~ hx_honesty_humility + hx_emotionality + hx_extraversion + hx_agreeableness + hx_conscientiousness + hx_openness, data = data),
  exploitative_risk_from_big_five = lm(outcome_exploitative_risk ~ bf_extraversion + bf_agreeableness + bf_conscientiousness + bf_neuroticism + bf_openness, data = data),
  exploitative_risk_from_hexaco = lm(outcome_exploitative_risk ~ hx_honesty_humility + hx_emotionality + hx_extraversion + hx_agreeableness + hx_conscientiousness + hx_openness, data = data),
  broad_functioning_from_big_five = lm(outcome_broad_functioning ~ bf_extraversion + bf_agreeableness + bf_conscientiousness + bf_neuroticism + bf_openness, data = data),
  broad_functioning_from_hexaco = lm(outcome_broad_functioning ~ hx_honesty_humility + hx_emotionality + hx_extraversion + hx_agreeableness + hx_conscientiousness + hx_openness, data = data)
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
  comparison = c("integrity_hexaco_minus_big_five_r2", "exploitative_risk_hexaco_minus_big_five_r2", "broad_functioning_hexaco_minus_big_five_r2"),
  delta_r2 = c(
    summary(models$integrity_from_hexaco)$r.squared - summary(models$integrity_from_big_five)$r.squared,
    summary(models$exploitative_risk_from_hexaco)$r.squared - summary(models$exploitative_risk_from_big_five)$r.squared,
    summary(models$broad_functioning_from_hexaco)$r.squared - summary(models$broad_functioning_from_big_five)$r.squared
  )
)

write.csv(summary(data[, c(bf, hx, facets, outcomes, derived)]), file.path(outputs, "r_alternative_structure_summary.csv"))
write.csv(cor(data[, c(bf, hx, facets, outcomes, derived)], use = "pairwise.complete.obs"), file.path(outputs, "r_alternative_structure_correlations.csv"))
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(delta_r2, file.path(outputs, "r_model_comparison_delta_r2.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_alternative_structure_items.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
