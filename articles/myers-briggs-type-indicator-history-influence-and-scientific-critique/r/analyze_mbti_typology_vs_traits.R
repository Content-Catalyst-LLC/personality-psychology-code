root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_mbti_typology_vs_traits.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

type_frequencies <- as.data.frame(table(data$type_code))
names(type_frequencies) <- c("type_code", "n")
type_frequencies$proportion <- type_frequencies$n / nrow(data)

context_summary <- aggregate(
  data[, c("near_boundary", "type_changed_on_retest", "boundary_risk_score", "information_loss_index", "collaboration_score", "reflective_utility_score")],
  by = list(assessment_context = data$assessment_context),
  FUN = mean
)

within_type_variation <- aggregate(
  data[, c("observed_ei", "observed_sn", "observed_tf", "observed_jp", "collaboration_score", "reflective_utility_score")],
  by = list(type_code = data$type_code),
  FUN = function(x) c(mean = mean(x), sd = sd(x), min = min(x), max = max(x))
)

boundary_cases <- data[data$near_boundary == 1, ]
boundary_cases <- boundary_cases[order(boundary_cases$min_absolute_distance_to_boundary), ]

model_continuous <- lm(
  collaboration_score ~ observed_ei + observed_sn + observed_tf + observed_jp,
  data = data
)

model_reflective <- lm(
  reflective_utility_score ~ observed_ei + observed_sn + observed_tf +
    observed_jp + boundary_risk_score,
  data = data
)

model_type <- lm(
  collaboration_score ~ type_code,
  data = data
)

model_comparison <- data.frame(
  model = c("continuous_dimensions", "type_categories"),
  r_squared = c(summary(model_continuous)$r.squared, summary(model_type)$r.squared),
  adjusted_r_squared = c(summary(model_continuous)$adj.r.squared, summary(model_type)$adj.r.squared)
)

type_change_summary <- data.frame(
  metric = c(
    "n",
    "near_boundary_n",
    "near_boundary_rate",
    "type_changed_on_retest_n",
    "type_changed_on_retest_rate",
    "mean_information_loss_index",
    "mean_boundary_risk_score"
  ),
  value = c(
    nrow(data),
    sum(data$near_boundary),
    mean(data$near_boundary),
    sum(data$type_changed_on_retest),
    mean(data$type_changed_on_retest),
    mean(data$information_loss_index),
    mean(data$boundary_risk_score)
  )
)

corr_cols <- c(
  "latent_ei", "latent_sn", "latent_tf", "latent_jp",
  "observed_ei", "observed_sn", "observed_tf", "observed_jp",
  "retest_ei", "retest_sn", "retest_tf", "retest_jp",
  "min_absolute_distance_to_boundary",
  "continuous_signal_strength",
  "boundary_risk_score",
  "information_loss_index",
  "collaboration_score",
  "reflective_utility_score"
)

write.csv(type_frequencies, file.path(outputs, "r_mbti_type_frequencies.csv"), row.names = FALSE)
write.csv(context_summary, file.path(outputs, "r_mbti_context_summary.csv"), row.names = FALSE)
write.csv(within_type_variation, file.path(outputs, "r_mbti_within_type_variation.csv"), row.names = FALSE)
write.csv(head(boundary_cases, 100), file.path(outputs, "r_mbti_boundary_cases_top100.csv"), row.names = FALSE)
write.csv(type_change_summary, file.path(outputs, "r_mbti_type_change_summary.csv"), row.names = FALSE)
write.csv(model_comparison, file.path(outputs, "r_mbti_model_comparison.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_mbti_dimensional_correlations.csv"))
capture.output(summary(model_continuous), file = file.path(outputs, "r_continuous_model_summary.txt"))
capture.output(summary(model_type), file = file.path(outputs, "r_type_model_summary.txt"))
capture.output(summary(model_reflective), file = file.path(outputs, "r_reflective_utility_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_mbti_typology_vs_traits.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
