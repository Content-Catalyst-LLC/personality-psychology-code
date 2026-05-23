args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_trait_hierarchies.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_hierarchical_trait_items.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

domains <- c("extraversion_score", "agreeableness_score", "conscientiousness_score", "neuroticism_score", "openness_score")
facets <- c("sociability_score", "assertiveness_score", "compassion_score", "politeness_score", "orderliness_score", "industriousness_score", "anxiety_score", "volatility_score", "aesthetics_score", "intellect_score")
outcomes <- c("broad_life_functioning", "focused_reliability_outcome", "creative_engagement_outcome")
derived <- c("bandwidth_fidelity_gap", "facet_profile_dispersion", "hierarchy_consistency_index")

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
  scale = c("conscientiousness_c1_c6", "orderliness_o1_o3", "industriousness_i1_i3", "broad_item_pool_item1_item60"),
  level = c("domain_item_set", "facet_item_set", "facet_item_set", "broad_item_pool"),
  n_items = c(6, 3, 3, 60),
  cronbach_alpha = c(
    alpha_score(data[, c("c1", "c2", "c3", "c4", "c5", "c6")]),
    alpha_score(data[, c("o1", "o2", "o3")]),
    alpha_score(data[, c("i1", "i2", "i3")]),
    alpha_score(data[, paste0("item", 1:60)])
  )
)

domain_model <- lm(broad_life_functioning ~ extraversion_score + agreeableness_score + conscientiousness_score + neuroticism_score + openness_score, data = data)
focused_domain_model <- lm(focused_reliability_outcome ~ conscientiousness_score, data = data)
focused_facet_model <- lm(focused_reliability_outcome ~ orderliness_score + industriousness_score, data = data)
creative_domain_model <- lm(creative_engagement_outcome ~ openness_score, data = data)
creative_facet_model <- lm(creative_engagement_outcome ~ aesthetics_score + intellect_score, data = data)

models <- list(
  broad_life_functioning_from_domains = domain_model,
  focused_reliability_from_domain = focused_domain_model,
  focused_reliability_from_facets = focused_facet_model,
  creative_engagement_from_domain = creative_domain_model,
  creative_engagement_from_facets = creative_facet_model
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

write.csv(summary(data[, c(domains, outcomes, derived)]), file.path(outputs, "r_domain_summary.csv"))
write.csv(summary(data[, c(facets, outcomes, derived)]), file.path(outputs, "r_facet_summary.csv"))
write.csv(cor(data[, c(domains, facets, outcomes, derived)], use = "pairwise.complete.obs"), file.path(outputs, "r_trait_hierarchy_correlations.csv"))
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_hierarchical_trait_items.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
