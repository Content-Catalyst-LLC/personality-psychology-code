# Personality, Wellbeing, and Mental Health
# R workflow for trait, distress, flourishing, and support analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_wellbeing_mental_health.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "participant_id",
  "age_band",
  "life_context",
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "coping_effectiveness",
  "perceived_support",
  "stress_burden",
  "positive_affect",
  "negative_affect",
  "life_satisfaction",
  "meaning_purpose",
  "wellbeing_score",
  "distress_score",
  "flourishing_score",
  "social_functioning",
  "treatment_access",
  "sleep_quality"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

data$regulation_support_index <- (
  data$conscientiousness +
  data$coping_effectiveness +
  data$perceived_support +
  data$sleep_quality -
  data$stress_burden
) / 4

data$flourishing_capacity_index <- (
  data$positive_affect +
  data$meaning_purpose +
  data$life_satisfaction +
  data$perceived_support -
  data$negative_affect
) / 4

data$distress_vulnerability_index <- (
  data$neuroticism +
  data$stress_burden +
  data$negative_affect -
  data$coping_effectiveness -
  data$perceived_support
)

data$distress_level <- ifelse(
  data$distress_score > median(data$distress_score, na.rm = TRUE),
  "higher_distress",
  "lower_distress"
)

data$flourishing_level <- ifelse(
  data$flourishing_score > median(data$flourishing_score, na.rm = TRUE),
  "higher_flourishing",
  "lower_flourishing"
)

data$mental_health_profile <- paste(
  data$distress_level,
  data$flourishing_level,
  sep = "_"
)

context_summary <- aggregate(
  data[, c("wellbeing_score", "distress_score", "flourishing_score", "perceived_support", "stress_burden", "treatment_access")],
  by = list(life_context = data$life_context),
  FUN = mean
)

context_n <- aggregate(
  data$participant_id,
  by = list(life_context = data$life_context),
  FUN = length
)
names(context_n)[2] <- "n"
context_summary <- merge(context_n, context_summary, by = "life_context")

write.csv(context_summary, file.path(outputs, "r_life_context_summary.csv"), row.names = FALSE)

profile_summary <- aggregate(
  data[, c("wellbeing_score", "distress_score", "flourishing_score", "neuroticism", "extraversion", "conscientiousness", "perceived_support")],
  by = list(mental_health_profile = data$mental_health_profile),
  FUN = mean
)

profile_n <- aggregate(
  data$participant_id,
  by = list(mental_health_profile = data$mental_health_profile),
  FUN = length
)
names(profile_n)[2] <- "n"
profile_summary <- merge(profile_n, profile_summary, by = "mental_health_profile")

write.csv(profile_summary, file.path(outputs, "r_two_continua_profile_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "coping_effectiveness",
  "perceived_support",
  "stress_burden",
  "positive_affect",
  "negative_affect",
  "life_satisfaction",
  "meaning_purpose",
  "wellbeing_score",
  "distress_score",
  "flourishing_score",
  "social_functioning"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_trait_wellbeing_correlations.csv"))

model_wb <- lm(
  wellbeing_score ~ extraversion + agreeableness +
    conscientiousness + neuroticism + openness +
    perceived_support + coping_effectiveness + sleep_quality,
  data = data
)

model_distress <- lm(
  distress_score ~ extraversion + agreeableness +
    conscientiousness + neuroticism + openness +
    stress_burden + perceived_support + sleep_quality,
  data = data
)

model_flourishing <- lm(
  flourishing_score ~ extraversion + agreeableness +
    conscientiousness + neuroticism + openness +
    meaning_purpose + perceived_support + coping_effectiveness,
  data = data
)

model_social <- lm(
  social_functioning ~ extraversion + agreeableness +
    conscientiousness + perceived_support + distress_score + sleep_quality,
  data = data
)

capture.output(summary(model_wb), file = file.path(outputs, "r_wellbeing_model_summary.txt"))
capture.output(summary(model_distress), file = file.path(outputs, "r_distress_model_summary.txt"))
capture.output(summary(model_flourishing), file = file.path(outputs, "r_flourishing_model_summary.txt"))
capture.output(summary(model_social), file = file.path(outputs, "r_social_functioning_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_wellbeing.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
