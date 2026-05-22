root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_motivation_goals_desire.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

data$ownership_level <- ifelse(
  data$goal_ownership > median(data$goal_ownership),
  "higher_ownership",
  "lower_ownership"
)
data$conflict_level <- ifelse(
  data$goal_conflict > median(data$goal_conflict),
  "higher_conflict",
  "lower_conflict"
)
data$meaning_level <- ifelse(
  data$meaning_goal > median(data$meaning_goal),
  "higher_meaning",
  "lower_meaning"
)
data$motivational_profile <- paste(
  data$ownership_level,
  data$conflict_level,
  data$meaning_level,
  sep = "_"
)

data$high_conflict_low_ownership <- data$goal_conflict > median(data$goal_conflict) &
  data$goal_ownership < median(data$goal_ownership)
data$high_status_low_meaning <- data$status_goal > median(data$status_goal) &
  data$meaning_goal < median(data$meaning_goal)

context_summary <- aggregate(
  data[, c("approach_orientation", "status_orientation", "avoidance_security_orientation", "need_support", "goal_ownership", "motivational_quality", "goal_conflict", "persistence_score", "adaptive_disengagement", "life_direction_coherence", "well_being")],
  by = list(motivation_context = data$motivation_context),
  FUN = mean
)

profile_summary <- aggregate(
  data[, c("goal_ownership", "goal_conflict", "meaning_goal", "need_support", "motivational_quality", "life_direction_coherence", "persistence_score", "adaptive_disengagement", "well_being")],
  by = list(motivational_profile = data$motivational_profile),
  FUN = mean
)

corr_cols <- c(
  "autonomy_goal", "achievement_goal", "belonging_goal", "security_goal", "meaning_goal", "status_goal",
  "goal_conflict", "goal_ownership", "autonomy_support", "competence_support", "relatedness_support",
  "need_support", "motivational_quality", "life_direction_coherence", "conscientiousness",
  "persistence_score", "adaptive_disengagement", "well_being"
)

model_persistence <- lm(
  persistence_score ~ autonomy_goal + achievement_goal + belonging_goal +
    security_goal + meaning_goal + status_goal +
    goal_conflict + goal_ownership + conscientiousness,
  data = data
)

model_conflict_buffer <- lm(
  persistence_score ~ goal_conflict * conscientiousness +
    goal_ownership + motivational_quality + need_support,
  data = data
)

model_wellbeing <- lm(
  well_being ~ motivational_quality + life_direction_coherence +
    goal_conflict + adaptive_disengagement + conscientiousness,
  data = data
)

model_disengagement <- lm(
  adaptive_disengagement ~ goal_conflict + goal_ownership +
    motivational_quality + conscientiousness,
  data = data
)

write.csv(context_summary, file.path(outputs, "r_motivation_context_summary.csv"), row.names = FALSE)
write.csv(profile_summary, file.path(outputs, "r_motivation_profile_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_motivation_goals_correlations.csv"))
capture.output(summary(model_persistence), file = file.path(outputs, "r_persistence_model_summary.txt"))
capture.output(summary(model_conflict_buffer), file = file.path(outputs, "r_conflict_buffer_model_summary.txt"))
capture.output(summary(model_wellbeing), file = file.path(outputs, "r_wellbeing_model_summary.txt"))
capture.output(summary(model_disengagement), file = file.path(outputs, "r_adaptive_disengagement_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_motivation_goals_desire.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
