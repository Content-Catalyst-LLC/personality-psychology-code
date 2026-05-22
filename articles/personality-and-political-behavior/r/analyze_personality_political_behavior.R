# Personality and Political Behavior
# R workflow for personality-politics analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_political_behavior.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "participant_id",
  "country_context",
  "political_system_type",
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "political_interest",
  "political_efficacy",
  "group_identity_strength",
  "perceived_threat",
  "media_exposure",
  "civic_opportunity",
  "ideology_score",
  "political_participation",
  "affective_polarization",
  "trust_in_institutions",
  "leadership_authority_preference"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

data$engagement_capacity <- (
  data$extraversion +
  data$political_interest +
  data$political_efficacy +
  data$civic_opportunity
) / 4

data$identity_threat_index <- (
  data$group_identity_strength +
  data$perceived_threat +
  data$media_exposure
) / 3

data$pluralism_openness_index <- (
  data$openness +
  data$agreeableness +
  data$trust_in_institutions -
  data$affective_polarization
) / 3

context_summary <- aggregate(
  data[, c("ideology_score", "political_participation", "affective_polarization", "trust_in_institutions", "engagement_capacity", "identity_threat_index")],
  by = list(country_context = data$country_context),
  FUN = mean
)

context_n <- aggregate(
  data$participant_id,
  by = list(country_context = data$country_context),
  FUN = length
)
names(context_n)[2] <- "n"
context_summary <- merge(context_n, context_summary, by = "country_context")

write.csv(context_summary, file.path(outputs, "r_context_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "political_interest",
  "political_efficacy",
  "group_identity_strength",
  "perceived_threat",
  "media_exposure",
  "civic_opportunity",
  "ideology_score",
  "political_participation",
  "affective_polarization",
  "trust_in_institutions",
  "leadership_authority_preference"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_trait_politics_correlations.csv"))

model_ideology <- lm(
  ideology_score ~ extraversion + agreeableness + conscientiousness +
    neuroticism + openness + group_identity_strength + perceived_threat +
    trust_in_institutions,
  data = data
)

model_participation <- lm(
  political_participation ~ extraversion + agreeableness + conscientiousness +
    neuroticism + openness + political_interest + political_efficacy +
    civic_opportunity,
  data = data
)

model_polarization <- lm(
  affective_polarization ~ group_identity_strength + perceived_threat +
    media_exposure + neuroticism + agreeableness +
    group_identity_strength:perceived_threat,
  data = data
)

model_authority <- lm(
  leadership_authority_preference ~ conscientiousness + neuroticism +
    perceived_threat + trust_in_institutions + openness,
  data = data
)

capture.output(summary(model_ideology), file = file.path(outputs, "r_ideology_model_summary.txt"))
capture.output(summary(model_participation), file = file.path(outputs, "r_participation_model_summary.txt"))
capture.output(summary(model_polarization), file = file.path(outputs, "r_polarization_model_summary.txt"))
capture.output(summary(model_authority), file = file.path(outputs, "r_authority_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_political_behavior.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
