root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_values_strivings_direction.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

data$transcendence_level <- ifelse(
  data$self_transcendence > median(data$self_transcendence),
  "higher_transcendence",
  "lower_transcendence"
)
data$enhancement_level <- ifelse(
  data$self_enhancement > median(data$self_enhancement),
  "higher_enhancement",
  "lower_enhancement"
)
data$conflict_level <- ifelse(
  data$striving_conflict > median(data$striving_conflict),
  "higher_conflict",
  "lower_conflict"
)
data$direction_profile <- paste(
  data$transcendence_level,
  data$enhancement_level,
  data$conflict_level,
  sep = "_"
)

data$high_conflict_low_ownership <- data$striving_conflict > median(data$striving_conflict) &
  data$striving_ownership < median(data$striving_ownership)
data$high_status_low_meaning <- data$striving_status > median(data$striving_status) &
  data$striving_meaning < median(data$striving_meaning)

context_summary <- aggregate(
  data[, c("self_transcendence", "self_enhancement", "openness_to_change", "conservation", "value_tension_total", "motivational_quality", "striving_conflict", "life_direction_coherence", "life_satisfaction")],
  by = list(value_context = data$value_context),
  FUN = mean
)

profile_summary <- aggregate(
  data[, c("self_transcendence", "self_enhancement", "motivational_quality", "striving_conflict", "life_direction_coherence", "life_satisfaction")],
  by = list(direction_profile = data$direction_profile),
  FUN = mean
)

corr_cols <- c(
  "benevolence", "universalism", "self_direction", "achievement", "power", "security", "tradition", "stimulation",
  "self_transcendence", "self_enhancement", "openness_to_change", "conservation",
  "value_tension_total", "striving_meaning", "striving_status", "striving_care",
  "striving_autonomy", "striving_competence", "striving_relatedness", "striving_conflict",
  "striving_ownership", "motivational_quality", "life_direction_coherence", "life_satisfaction"
)

model_life_satisfaction <- lm(
  life_satisfaction ~ self_transcendence + self_enhancement +
    openness_to_change + conservation + striving_meaning +
    striving_status + striving_care + motivational_quality +
    striving_conflict,
  data = data
)

model_buffer <- lm(
  life_satisfaction ~ striving_conflict * motivational_quality +
    self_transcendence + self_enhancement +
    openness_to_change + conservation,
  data = data
)

model_direction <- lm(
  life_direction_coherence ~ self_transcendence +
    openness_to_change + striving_ownership +
    striving_conflict + value_tension_total,
  data = data
)

write.csv(context_summary, file.path(outputs, "r_values_strivings_context_summary.csv"), row.names = FALSE)
write.csv(profile_summary, file.path(outputs, "r_values_strivings_direction_profile_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_values_strivings_correlations.csv"))
capture.output(summary(model_life_satisfaction), file = file.path(outputs, "r_life_satisfaction_model_summary.txt"))
capture.output(summary(model_buffer), file = file.path(outputs, "r_conflict_buffer_model_summary.txt"))
capture.output(summary(model_direction), file = file.path(outputs, "r_life_direction_coherence_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_values_strivings_direction.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
