args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1])) else normalizePath("r/analyze_lexical_structure.R")
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_lexical_descriptors.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

descriptors <- paste0("adj", 1:100)
clusters <- c("sociable_cluster_score", "reliable_cluster_score", "compassionate_cluster_score", "anxious_cluster_score", "imaginative_cluster_score")
criteria <- c("social_reliability_outcome", "interpersonal_trust_outcome", "expressive_engagement_outcome", "lexical_visibility_index")
derived <- c("lexical_abundance_index", "structural_centrality_index", "descriptor_redundancy_index", "cross_language_caution_index")

alpha_score <- function(df) {
  k <- ncol(df)
  item_vars <- apply(df, 2, var)
  total_var <- var(rowSums(df))
  (k / (k - 1)) * (1 - sum(item_vars) / total_var)
}

data$sociable_rescored <- rowMeans(data[, paste0("adj", 1:20)])
data$reliable_rescored <- rowMeans(data[, paste0("adj", 21:40)])
data$compassionate_rescored <- rowMeans(data[, paste0("adj", 41:60)])
data$anxious_rescored <- rowMeans(data[, paste0("adj", 61:80)])
data$imaginative_rescored <- rowMeans(data[, paste0("adj", 81:100)])

reliability <- data.frame(
  scale = c(
    "sociable_descriptor_block_adj1_adj20",
    "reliable_descriptor_block_adj21_adj40",
    "compassionate_descriptor_block_adj41_adj60",
    "anxious_descriptor_block_adj61_adj80",
    "imaginative_descriptor_block_adj81_adj100",
    "full_lexical_descriptor_pool_adj1_adj100"
  ),
  level = c(rep("descriptor_cluster", 5), "full_descriptor_pool"),
  n_items = c(20, 20, 20, 20, 20, 100),
  cronbach_alpha = c(
    alpha_score(data[, paste0("adj", 1:20)]),
    alpha_score(data[, paste0("adj", 21:40)]),
    alpha_score(data[, paste0("adj", 41:60)]),
    alpha_score(data[, paste0("adj", 61:80)]),
    alpha_score(data[, paste0("adj", 81:100)]),
    alpha_score(data[, descriptors])
  )
)

# Principal components using base R.
descriptor_scaled <- scale(data[, descriptors])
pca <- prcomp(descriptor_scaled, center = FALSE, scale. = FALSE)
component_scores <- as.data.frame(pca$x[, 1:10])
names(component_scores) <- paste0("lexical_component_", 1:10)
data <- cbind(data, component_scores)

pca_summary <- data.frame(
  component = 1:10,
  explained_variance_ratio = (pca$sdev[1:10]^2) / sum(pca$sdev^2),
  cumulative_explained_variance = cumsum((pca$sdev[1:10]^2) / sum(pca$sdev^2))
)

models <- list(
  social_reliability_from_clusters = lm(social_reliability_outcome ~ reliable_cluster_score + compassionate_cluster_score + anxious_cluster_score, data = data),
  interpersonal_trust_from_clusters = lm(interpersonal_trust_outcome ~ compassionate_cluster_score + sociable_cluster_score + anxious_cluster_score, data = data),
  expressive_engagement_from_clusters = lm(expressive_engagement_outcome ~ sociable_cluster_score + imaginative_cluster_score + anxious_cluster_score, data = data),
  lexical_visibility_from_components = lm(lexical_visibility_index ~ lexical_component_1 + lexical_component_2 + lexical_component_3 + lexical_component_4 + lexical_component_5, data = data),
  structural_centrality_from_abundance_and_redundancy = lm(structural_centrality_index ~ lexical_abundance_index + descriptor_redundancy_index + cross_language_caution_index, data = data)
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

five_component_model <- lm(social_reliability_outcome ~ lexical_component_1 + lexical_component_2 + lexical_component_3 + lexical_component_4 + lexical_component_5, data = data)
six_component_model <- lm(social_reliability_outcome ~ lexical_component_1 + lexical_component_2 + lexical_component_3 + lexical_component_4 + lexical_component_5 + lexical_component_6, data = data)
component_comparison <- data.frame(
  comparison = "six_minus_five_components_social_reliability_r2",
  delta_r2 = summary(six_component_model)$r.squared - summary(five_component_model)$r.squared
)

write.csv(summary(data[, c(clusters, criteria, derived)]), file.path(outputs, "r_cluster_summary.csv"))
write.csv(cor(data[, c(clusters, criteria, derived)], use = "pairwise.complete.obs"), file.path(outputs, "r_lexical_cluster_correlations.csv"))
write.csv(pca_summary, file.path(outputs, "r_pca_dimensionality_summary.csv"), row.names = FALSE)
write.csv(reliability, file.path(outputs, "r_reliability_summary.csv"), row.names = FALSE)
write.csv(model_fit, file.path(outputs, "r_model_fit_summary.csv"), row.names = FALSE)
write.csv(model_coefficients, file.path(outputs, "r_model_coefficients.csv"), row.names = FALSE)
write.csv(component_comparison, file.path(outputs, "r_five_six_component_comparison.csv"), row.names = FALSE)
write.csv(data, file.path(outputs, "r_scored_lexical_descriptors.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
