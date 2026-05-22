root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_types_traits_dimensional_models.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

trait_cols <- c(
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness"
)

context_summary <- aggregate(
  data[, c("near_threshold_boundary", "near_cluster_boundary", "information_loss_index", "dimensional_signal_strength", "well_being", "collaboration_score", "reflective_utility_score")],
  by = list(assessment_context = data$assessment_context),
  FUN = mean
)

profile_summary <- aggregate(
  data[, c("extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness", "well_being", "collaboration_score", "information_loss_index")],
  by = list(profile_type = data$profile_type),
  FUN = mean
)

cluster_summary <- aggregate(
  data[, c("extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness", "near_cluster_boundary", "well_being", "collaboration_score")],
  by = list(synthetic_cluster = data$synthetic_cluster),
  FUN = mean
)

type_counts <- as.data.frame(table(data$profile_type))
names(type_counts) <- c("profile_type", "n")
type_counts$proportion <- type_counts$n / nrow(data)

boundary_cases <- data[data$near_threshold_boundary == 1 | data$near_cluster_boundary == 1, ]
boundary_cases <- boundary_cases[order(boundary_cases$nearest_threshold_distance, boundary_cases$cluster_boundary_margin), ]

model_dimensional <- lm(
  well_being ~ extraversion + agreeableness + conscientiousness +
    neuroticism + openness,
  data = data
)

model_profile <- lm(
  well_being ~ profile_type,
  data = data
)

model_cluster <- lm(
  well_being ~ synthetic_cluster,
  data = data
)

model_combined <- lm(
  well_being ~ extraversion + agreeableness + conscientiousness +
    neuroticism + openness + synthetic_cluster,
  data = data
)

model_comparison <- data.frame(
  model = c("dimensional_traits", "profile_type_categories", "cluster_categories", "combined_traits_plus_cluster"),
  r_squared = c(
    summary(model_dimensional)$r.squared,
    summary(model_profile)$r.squared,
    summary(model_cluster)$r.squared,
    summary(model_combined)$r.squared
  ),
  adjusted_r_squared = c(
    summary(model_dimensional)$adj.r.squared,
    summary(model_profile)$adj.r.squared,
    summary(model_cluster)$adj.r.squared,
    summary(model_combined)$adj.r.squared
  )
)

corr_cols <- c(
  trait_cols,
  "nearest_threshold_distance",
  "near_threshold_boundary",
  "cluster_boundary_margin",
  "near_cluster_boundary",
  "dimensional_signal_strength",
  "information_loss_index",
  "well_being",
  "collaboration_score",
  "reflective_utility_score"
)

write.csv(context_summary, file.path(outputs, "r_context_summary.csv"), row.names = FALSE)
write.csv(profile_summary, file.path(outputs, "r_profile_type_summary.csv"), row.names = FALSE)
write.csv(cluster_summary, file.path(outputs, "r_cluster_summary.csv"), row.names = FALSE)
write.csv(type_counts, file.path(outputs, "r_profile_type_counts.csv"), row.names = FALSE)
write.csv(head(boundary_cases, 100), file.path(outputs, "r_boundary_cases_top100.csv"), row.names = FALSE)
write.csv(model_comparison, file.path(outputs, "r_model_comparison.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_dimensional_correlations.csv"))
capture.output(summary(model_dimensional), file = file.path(outputs, "r_dimensional_model_summary.txt"))
capture.output(summary(model_profile), file = file.path(outputs, "r_profile_model_summary.txt"))
capture.output(summary(model_cluster), file = file.path(outputs, "r_cluster_model_summary.txt"))
capture.output(summary(model_combined), file = file.path(outputs, "r_combined_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_types_traits_dimensional_models.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
