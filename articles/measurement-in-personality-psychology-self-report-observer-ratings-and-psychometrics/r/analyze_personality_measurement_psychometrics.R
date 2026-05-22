root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_measurement_data.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

self_items <- c("s1", "s2", "s3", "s4", "s5")
observer_items <- c("o1", "o2", "o3", "o4", "o5")

cronbach_alpha <- function(df_items) {
  clean <- na.omit(df_items)
  k <- ncol(clean)
  if (nrow(clean) < 3 || k < 2) return(NA_real_)
  item_var <- sum(apply(clean, 2, var))
  total_var <- var(rowSums(clean))
  (k / (k - 1)) * (1 - item_var / total_var)
}

self_alpha <- cronbach_alpha(data[, self_items])
observer_alpha <- cronbach_alpha(data[, observer_items])

self_other_agreement <- cor(
  data$self_conscientiousness,
  data$observer_conscientiousness,
  use = "pairwise.complete.obs"
)

filtered <- data[
  data$attention_check == 1 &
    data$self_missing_count <= 2 &
    data$observer_missing_count <= 2,
]

filtered_agreement <- cor(
  filtered$self_conscientiousness,
  filtered$observer_conscientiousness,
  use = "pairwise.complete.obs"
)

context_summary <- aggregate(
  data[, c("attention_check", "careless_response_risk", "social_desirability_pressure", "self_conscientiousness", "observer_conscientiousness", "absolute_self_other_discrepancy", "method_effect_index", "reliability_context_score", "professional_reflection_score")],
  by = list(assessment_context = data$assessment_context),
  FUN = mean,
  na.rm = TRUE
)

item_summary <- data.frame(
  item = c(self_items, observer_items),
  source = c(rep("self_report", length(self_items)), rep("observer_report", length(observer_items))),
  mean = sapply(data[, c(self_items, observer_items)], mean, na.rm = TRUE),
  sd = sapply(data[, c(self_items, observer_items)], sd, na.rm = TRUE),
  missing_rate = sapply(data[, c(self_items, observer_items)], function(x) mean(is.na(x)))
)

reliability_summary <- data.frame(
  metric = c(
    "n",
    "self_report_alpha",
    "observer_report_alpha",
    "self_other_agreement",
    "filtered_self_other_agreement",
    "mean_absolute_self_other_discrepancy",
    "attention_pass_rate",
    "mean_method_effect_index"
  ),
  value = c(
    nrow(data),
    self_alpha,
    observer_alpha,
    self_other_agreement,
    filtered_agreement,
    mean(data$absolute_self_other_discrepancy, na.rm = TRUE),
    mean(data$attention_check, na.rm = TRUE),
    mean(data$method_effect_index, na.rm = TRUE)
  )
)

model_agreement <- lm(
  observer_conscientiousness ~ self_conscientiousness,
  data = data
)

model_discrepancy <- lm(
  absolute_self_other_discrepancy ~ careless_response_risk +
    social_desirability_pressure + method_effect_index,
  data = data
)

model_professional <- lm(
  professional_reflection_score ~ reliability_context_score +
    method_effect_index + absolute_self_other_discrepancy,
  data = data
)

corr_cols <- c(
  self_items,
  observer_items,
  "self_conscientiousness",
  "observer_conscientiousness",
  "self_other_discrepancy",
  "absolute_self_other_discrepancy",
  "careless_response_risk",
  "social_desirability_pressure",
  "method_effect_index",
  "reliability_context_score",
  "professional_reflection_score"
)

write.csv(context_summary, file.path(outputs, "r_context_summary.csv"), row.names = FALSE)
write.csv(item_summary, file.path(outputs, "r_item_summary.csv"), row.names = FALSE)
write.csv(reliability_summary, file.path(outputs, "r_reliability_agreement_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_measurement_correlations.csv"))
capture.output(summary(model_agreement), file = file.path(outputs, "r_agreement_model_summary.txt"))
capture.output(summary(model_discrepancy), file = file.path(outputs, "r_discrepancy_model_summary.txt"))
capture.output(summary(model_professional), file = file.path(outputs, "r_professional_reflection_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_personality_measurement_data.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
