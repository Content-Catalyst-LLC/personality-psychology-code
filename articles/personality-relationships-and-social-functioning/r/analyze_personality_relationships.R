# Personality, Relationships, and Social Functioning
# R workflow for relational-personality analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_relationships_social_functioning.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "participant_id",
  "social_context",
  "relationship_domain",
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "empathy",
  "self_regulation",
  "attachment_security",
  "perceived_support",
  "relationship_satisfaction",
  "social_functioning",
  "loneliness",
  "conflict_frequency",
  "reciprocity_quality",
  "reputation_trust"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

data$relational_stability_index <- (
  data$agreeableness +
  data$conscientiousness +
  data$empathy +
  data$self_regulation +
  data$attachment_security -
  data$neuroticism
) / 5

data$social_support_index <- (
  data$perceived_support +
  data$relationship_satisfaction +
  data$social_functioning -
  data$loneliness
) / 3

data$conflict_risk_index <- (
  data$neuroticism +
  data$conflict_frequency -
  data$agreeableness -
  data$self_regulation
)

context_summary <- aggregate(
  data[, c("relationship_satisfaction", "social_functioning", "loneliness", "conflict_frequency", "perceived_support", "relational_stability_index")],
  by = list(social_context = data$social_context),
  FUN = mean
)

context_n <- aggregate(
  data$participant_id,
  by = list(social_context = data$social_context),
  FUN = length
)
names(context_n)[2] <- "n"
context_summary <- merge(context_n, context_summary, by = "social_context")

write.csv(context_summary, file.path(outputs, "r_social_context_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "extraversion",
  "agreeableness",
  "conscientiousness",
  "neuroticism",
  "openness",
  "empathy",
  "self_regulation",
  "attachment_security",
  "perceived_support",
  "relationship_satisfaction",
  "social_functioning",
  "loneliness",
  "conflict_frequency",
  "reciprocity_quality",
  "reputation_trust"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_trait_relationship_correlations.csv"))

model_rel <- lm(
  relationship_satisfaction ~ extraversion + agreeableness +
    conscientiousness + neuroticism + openness +
    empathy + self_regulation + attachment_security,
  data = data
)

model_soc <- lm(
  social_functioning ~ extraversion + agreeableness +
    conscientiousness + neuroticism + openness +
    empathy + self_regulation + perceived_support,
  data = data
)

model_lonely <- lm(
  loneliness ~ extraversion + agreeableness + neuroticism +
    attachment_security + perceived_support,
  data = data
)

model_conflict <- lm(
  conflict_frequency ~ agreeableness + neuroticism +
    self_regulation + attachment_security,
  data = data
)

capture.output(summary(model_rel), file = file.path(outputs, "r_relationship_satisfaction_model_summary.txt"))
capture.output(summary(model_soc), file = file.path(outputs, "r_social_functioning_model_summary.txt"))
capture.output(summary(model_lonely), file = file.path(outputs, "r_loneliness_model_summary.txt"))
capture.output(summary(model_conflict), file = file.path(outputs, "r_conflict_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_relationships.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
