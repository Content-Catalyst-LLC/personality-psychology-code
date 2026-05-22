# Personality, Work, and Leadership
# R workflow for personality and occupational outcomes

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_work_leadership.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "participant_id",
  "role_family",
  "organizational_context",
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "emotional_stability",
  "dark_trait_pressure",
  "role_fit",
  "accountability",
  "job_performance",
  "leadership_emergence",
  "leadership_effectiveness",
  "counterproductive_work_behavior",
  "teamwork_quality",
  "burnout_risk"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

data$dependability_index <- (
  data$conscientiousness +
  data$emotional_stability +
  data$role_fit
) / 3

data$leadership_stewardship_index <- (
  data$conscientiousness +
  data$agreeableness +
  data$emotional_stability +
  data$accountability -
  data$dark_trait_pressure
) / 4

data$derailment_risk_index <- (
  data$dark_trait_pressure +
  data$neuroticism -
  data$accountability -
  data$role_fit
)

role_summary <- aggregate(
  data[, c("job_performance", "leadership_emergence", "leadership_effectiveness", "teamwork_quality", "burnout_risk", "leadership_stewardship_index", "derailment_risk_index")],
  by = list(role_family = data$role_family),
  FUN = mean
)

role_n <- aggregate(
  data$participant_id,
  by = list(role_family = data$role_family),
  FUN = length
)
names(role_n)[2] <- "n"
role_summary <- merge(role_n, role_summary, by = "role_family")

write.csv(role_summary, file.path(outputs, "r_role_family_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "emotional_stability",
  "dark_trait_pressure",
  "role_fit",
  "accountability",
  "dependability_index",
  "leadership_stewardship_index",
  "derailment_risk_index",
  "job_performance",
  "leadership_emergence",
  "leadership_effectiveness",
  "counterproductive_work_behavior",
  "teamwork_quality",
  "burnout_risk"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_trait_work_correlations.csv"))

model_perf <- lm(
  job_performance ~ extraversion + agreeableness + conscientiousness +
    emotional_stability + openness + role_fit,
  data = data
)

model_emergence <- lm(
  leadership_emergence ~ extraversion + openness + emotional_stability + role_fit,
  data = data
)

model_effectiveness <- lm(
  leadership_effectiveness ~ conscientiousness + agreeableness +
    emotional_stability + openness + role_fit + accountability,
  data = data
)

model_cwb <- lm(
  counterproductive_work_behavior ~ dark_trait_pressure + neuroticism +
    agreeableness + conscientiousness + accountability,
  data = data
)

capture.output(summary(model_perf), file = file.path(outputs, "r_performance_model_summary.txt"))
capture.output(summary(model_emergence), file = file.path(outputs, "r_leadership_emergence_model_summary.txt"))
capture.output(summary(model_effectiveness), file = file.path(outputs, "r_leadership_effectiveness_model_summary.txt"))
capture.output(summary(model_cwb), file = file.path(outputs, "r_cwb_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_work_leadership.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
