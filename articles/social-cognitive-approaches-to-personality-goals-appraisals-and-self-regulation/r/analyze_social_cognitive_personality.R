root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_social_cognitive_personality.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

processes <- c(
  "goal_activation",
  "threat_appraisal",
  "challenge_appraisal",
  "self_efficacy",
  "self_regulation",
  "emotional_arousal",
  "perceived_support"
)

outcomes <- c("prosocial_behavior", "avoidance_behavior", "task_persistence")
derived <- c("appraisal_balance", "regulation_capacity", "approach_orientation", "avoidance_pressure")

person_summary <- aggregate(
  data[, c(processes, outcomes)],
  by = list(person_id = data$person_id),
  FUN = mean
)
write.csv(person_summary, file.path(outputs, "r_person_summary.csv"), row.names = FALSE)

situation_summary <- aggregate(
  data[, c(processes, outcomes)],
  by = list(situation_type = data$situation_type),
  FUN = mean
)
write.csv(situation_summary, file.path(outputs, "r_situation_summary.csv"), row.names = FALSE)

corr_cols <- c(processes, derived, outcomes)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_social_cognitive_correlations.csv"))

model_prosocial <- lm(
  prosocial_behavior ~ goal_activation + threat_appraisal + challenge_appraisal +
    self_efficacy + self_regulation + emotional_arousal + perceived_support,
  data = data
)

model_avoidance <- lm(
  avoidance_behavior ~ goal_activation + threat_appraisal + challenge_appraisal +
    self_efficacy + self_regulation + emotional_arousal + perceived_support,
  data = data
)

model_persistence <- lm(
  task_persistence ~ goal_activation + threat_appraisal + challenge_appraisal +
    self_efficacy + self_regulation + emotional_arousal + perceived_support,
  data = data
)

capture.output(summary(model_prosocial), file = file.path(outputs, "r_prosocial_behavior_model_summary.txt"))
capture.output(summary(model_avoidance), file = file.path(outputs, "r_avoidance_behavior_model_summary.txt"))
capture.output(summary(model_persistence), file = file.path(outputs, "r_task_persistence_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_social_cognitive_personality.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
