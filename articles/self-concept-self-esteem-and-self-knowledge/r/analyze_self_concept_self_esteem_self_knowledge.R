root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_self_concept_self_esteem_self_knowledge.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

agreement_summary <- data.frame(
  domain = c("warmth", "conscientiousness", "emotional_stability", "openness"),
  self_other_agreement = c(
    cor(data$self_warmth, data$other_warmth, use = "pairwise.complete.obs"),
    cor(data$self_conscientiousness, data$other_conscientiousness, use = "pairwise.complete.obs"),
    cor(data$self_emotional_stability, data$other_emotional_stability, use = "pairwise.complete.obs"),
    cor(data$self_openness, data$other_openness, use = "pairwise.complete.obs")
  )
)

data$esteem_level <- ifelse(
  data$self_esteem > median(data$self_esteem),
  "higher_self_esteem",
  "lower_self_esteem"
)
data$accuracy_level <- ifelse(
  data$self_knowledge_accuracy > median(data$self_knowledge_accuracy),
  "higher_self_knowledge",
  "lower_self_knowledge"
)
data$discrepancy_level <- ifelse(
  data$total_self_discrepancy > median(data$total_self_discrepancy),
  "higher_discrepancy",
  "lower_discrepancy"
)
data$self_system_profile <- paste(
  data$esteem_level,
  data$accuracy_level,
  data$discrepancy_level,
  sep = "_"
)

data$high_esteem_low_accuracy <- data$self_esteem > median(data$self_esteem) &
  data$self_knowledge_accuracy < median(data$self_knowledge_accuracy)
data$low_esteem_high_devaluation <- data$self_esteem < median(data$self_esteem) &
  data$external_devaluation > median(data$external_devaluation)

context_summary <- aggregate(
  data[, c("self_concept_positivity", "self_esteem", "self_knowledge_accuracy", "total_self_discrepancy", "social_recognition", "external_devaluation", "well_being")],
  by = list(self_system_context = data$self_system_context),
  FUN = mean
)

profile_summary <- aggregate(
  data[, c("self_esteem", "self_knowledge_accuracy", "total_self_discrepancy", "social_recognition", "external_devaluation", "well_being")],
  by = list(self_system_profile = data$self_system_profile),
  FUN = mean
)

corr_cols <- c(
  "self_warmth", "self_conscientiousness", "self_emotional_stability", "self_openness",
  "other_warmth", "other_conscientiousness", "other_emotional_stability", "other_openness",
  "actual_self", "ideal_self", "ought_self", "self_esteem", "social_recognition",
  "external_devaluation", "well_being", "self_other_gap_mean", "self_knowledge_accuracy",
  "actual_ideal_discrepancy", "actual_ought_discrepancy", "total_self_discrepancy",
  "self_concept_positivity"
)

model_self_esteem <- lm(
  self_esteem ~ self_concept_positivity + total_self_discrepancy +
    self_knowledge_accuracy + social_recognition + external_devaluation,
  data = data
)

model_wellbeing <- lm(
  well_being ~ self_esteem + total_self_discrepancy +
    self_knowledge_accuracy + social_recognition + external_devaluation,
  data = data
)

model_accuracy <- lm(
  self_knowledge_accuracy ~ social_recognition + external_devaluation +
    self_concept_positivity + self_esteem,
  data = data
)

write.csv(context_summary, file.path(outputs, "r_self_system_context_summary.csv"), row.names = FALSE)
write.csv(agreement_summary, file.path(outputs, "r_self_other_agreement_summary.csv"), row.names = FALSE)
write.csv(profile_summary, file.path(outputs, "r_self_system_profile_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_self_system_correlations.csv"))
capture.output(summary(model_self_esteem), file = file.path(outputs, "r_self_esteem_model_summary.txt"))
capture.output(summary(model_wellbeing), file = file.path(outputs, "r_wellbeing_model_summary.txt"))
capture.output(summary(model_accuracy), file = file.path(outputs, "r_self_knowledge_accuracy_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_self_concept_self_esteem_self_knowledge.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
