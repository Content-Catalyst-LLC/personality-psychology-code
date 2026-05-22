# Personality and Physical Health Across the Lifespan
# R workflow for longitudinal personality-health analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_physical_health_lifespan.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "person_id",
  "wave",
  "age",
  "age_band",
  "life_context",
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "emotional_stability",
  "perceived_support",
  "exercise",
  "sleep_quality",
  "smoking_risk",
  "alcohol_risk",
  "medication_adherence",
  "stress_burden",
  "physical_health_score",
  "functional_ability",
  "chronic_condition_burden"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

data$health_behavior_index <- (
  data$exercise +
  data$sleep_quality +
  data$medication_adherence -
  data$smoking_risk -
  data$alcohol_risk
) / 3

data$stress_vulnerability_index <- (
  data$neuroticism +
  data$stress_burden -
  data$emotional_stability -
  data$perceived_support
)

data$healthy_aging_support_index <- (
  data$physical_health_score +
  data$functional_ability +
  data$perceived_support +
  data$medication_adherence
) / 4

data$healthy_neuroticism_index <- (
  data$neuroticism * data$conscientiousness
) / 7

age_summary <- aggregate(
  data[, c("physical_health_score", "functional_ability", "chronic_condition_burden", "health_behavior_index", "stress_vulnerability_index")],
  by = list(age_band = data$age_band),
  FUN = mean
)

age_n <- aggregate(
  data$person_id,
  by = list(age_band = data$age_band),
  FUN = length
)
names(age_n)[2] <- "observations"
age_summary <- merge(age_n, age_summary, by = "age_band")

write.csv(age_summary, file.path(outputs, "r_age_band_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "emotional_stability",
  "perceived_support",
  "exercise",
  "sleep_quality",
  "smoking_risk",
  "alcohol_risk",
  "medication_adherence",
  "stress_burden",
  "physical_health_score",
  "functional_ability",
  "chronic_condition_burden"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_trait_health_correlations.csv"))

model_health <- lm(
  physical_health_score ~ conscientiousness + neuroticism + extraversion +
    openness + exercise + sleep_quality + smoking_risk +
    medication_adherence + stress_burden + age + wave,
  data = data
)

model_healthy_neuroticism <- lm(
  physical_health_score ~ neuroticism * conscientiousness +
    exercise + sleep_quality + smoking_risk +
    medication_adherence + stress_burden + age + wave,
  data = data
)

model_function <- lm(
  functional_ability ~ physical_health_score + conscientiousness +
    emotional_stability + perceived_support + medication_adherence +
    age + wave,
  data = data
)

model_chronic <- lm(
  chronic_condition_burden ~ age + stress_burden + smoking_risk +
    alcohol_risk + conscientiousness + physical_health_score +
    perceived_support,
  data = data
)

capture.output(summary(model_health), file = file.path(outputs, "r_physical_health_model_summary.txt"))
capture.output(summary(model_healthy_neuroticism), file = file.path(outputs, "r_healthy_neuroticism_model_summary.txt"))
capture.output(summary(model_function), file = file.path(outputs, "r_functional_ability_model_summary.txt"))
capture.output(summary(model_chronic), file = file.path(outputs, "r_chronic_condition_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_physical_health.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
