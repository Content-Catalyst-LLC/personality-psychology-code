root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_traits_character_morality.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

traits <- c("honesty_humility", "conscientiousness", "agreeableness", "emotional_stability", "openness")
outcomes <- c("ethical_behavior", "integrity_rating", "trustworthiness_rating")

data$descriptive_trait_reliability <- rowMeans(data[, c("honesty_humility", "conscientiousness", "agreeableness")])
data$moral_character_index <- rowMeans(data[, outcomes])
data$judgment_context_index <- rowMeans(data[, c("practical_judgment", "institutional_accountability")])
data$trait_character_gap <- data$moral_character_index - data$descriptive_trait_reliability
data$trait_character_profile <- paste(
  ifelse(data$descriptive_trait_reliability > median(data$descriptive_trait_reliability), "higher_trait_reliability", "lower_trait_reliability"),
  ifelse(data$moral_character_index > median(data$moral_character_index), "higher_character_evaluation", "lower_character_evaluation"),
  sep = "_"
)

context_summary <- aggregate(
  data[, c("descriptive_trait_reliability", "moral_character_index", "moral_identity", "practical_judgment", "institutional_accountability", "power_pressure")],
  by = list(evaluation_context = data$evaluation_context),
  FUN = mean
)
write.csv(context_summary, file.path(outputs, "r_evaluation_context_summary.csv"), row.names = FALSE)

profile_summary <- aggregate(
  data[, c("descriptive_trait_reliability", "moral_character_index", "moral_identity", "practical_judgment", "institutional_accountability")],
  by = list(trait_character_profile = data$trait_character_profile),
  FUN = mean
)
write.csv(profile_summary, file.path(outputs, "r_trait_character_profile_summary.csv"), row.names = FALSE)

corr_cols <- c(traits, "moral_identity", "practical_judgment", "institutional_accountability", "power_pressure", "social_desirability_pressure", outcomes, "descriptive_trait_reliability", "moral_character_index", "judgment_context_index", "trait_character_gap")
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_traits_character_correlations.csv"))

model_ethical <- lm(ethical_behavior ~ honesty_humility + conscientiousness + agreeableness + emotional_stability + openness + moral_identity, data = data)
model_character <- lm(moral_character_index ~ descriptive_trait_reliability + moral_identity + practical_judgment + institutional_accountability, data = data)
model_gap <- lm(trait_character_gap ~ moral_identity + practical_judgment + institutional_accountability + power_pressure + social_desirability_pressure, data = data)

capture.output(summary(model_ethical), file = file.path(outputs, "r_ethical_behavior_model_summary.txt"))
capture.output(summary(model_character), file = file.path(outputs, "r_moral_character_model_summary.txt"))
capture.output(summary(model_gap), file = file.path(outputs, "r_trait_character_gap_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_traits_character_morality.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
