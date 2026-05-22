root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_dark_traits_virtue_personality.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)
dark <- c("machiavellianism", "narcissism", "psychopathy", "sadism")
virtue <- c("honesty_humility", "conscientious_reliability", "fairness_orientation", "compassion_kindness")

data$dark_trait_burden <- rowMeans(data[, dark])
data$virtue_relevant_tendency <- rowMeans(data[, virtue])
data$moral_integration_index <- rowMeans(data[, c("virtue_relevant_tendency", "moral_identity", "practical_judgment")])
data$dark_accountability_risk <- data$dark_trait_burden * (7 - data$institutional_accountability)
data$dominant_dark_trait <- dark[max.col(data[, dark], ties.method = "first")]
data$moral_profile <- paste(
  ifelse(data$dark_trait_burden > median(data$dark_trait_burden), "higher_darkness", "lower_darkness"),
  ifelse(data$virtue_relevant_tendency > median(data$virtue_relevant_tendency), "higher_virtue_relevant", "lower_virtue_relevant"),
  sep = "_"
)

context_summary <- aggregate(
  data[, c("dark_trait_burden", "virtue_relevant_tendency", "institutional_accountability", "status_reward_pressure", "unethical_behavior", "prosocial_restraint", "harm_indicator")],
  by = list(institutional_context = data$institutional_context),
  FUN = mean
)
write.csv(context_summary, file.path(outputs, "r_institutional_context_summary.csv"), row.names = FALSE)

profile_summary <- aggregate(
  data[, c("dark_trait_burden", "virtue_relevant_tendency", "moral_integration_index", "unethical_behavior", "prosocial_restraint", "harm_indicator")],
  by = list(moral_profile = data$moral_profile),
  FUN = mean
)
write.csv(profile_summary, file.path(outputs, "r_moral_profile_summary.csv"), row.names = FALSE)

corr_cols <- c(dark, virtue, "moral_identity", "practical_judgment", "institutional_accountability", "status_reward_pressure", "unethical_behavior", "prosocial_restraint", "harm_indicator", "dark_trait_burden", "virtue_relevant_tendency", "moral_integration_index", "dark_accountability_risk")
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_dark_traits_virtue_correlations.csv"))

model_unethical <- lm(unethical_behavior ~ machiavellianism + narcissism + psychopathy + sadism + honesty_humility + conscientious_reliability + fairness_orientation + compassion_kindness, data = data)
model_prosocial <- lm(prosocial_restraint ~ dark_trait_burden + virtue_relevant_tendency + moral_identity + practical_judgment, data = data)
model_harm <- lm(harm_indicator ~ dark_trait_burden + virtue_relevant_tendency + institutional_accountability + status_reward_pressure + dark_accountability_risk, data = data)

capture.output(summary(model_unethical), file = file.path(outputs, "r_unethical_behavior_model_summary.txt"))
capture.output(summary(model_prosocial), file = file.path(outputs, "r_prosocial_restraint_model_summary.txt"))
capture.output(summary(model_harm), file = file.path(outputs, "r_harm_indicator_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_dark_traits_virtue.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
