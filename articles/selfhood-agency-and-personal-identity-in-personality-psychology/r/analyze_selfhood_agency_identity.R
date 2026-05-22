root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_selfhood_agency_identity.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

data$continuity_level <- ifelse(
  data$temporal_self_continuity > median(data$temporal_self_continuity),
  "higher_continuity",
  "lower_continuity"
)
data$agency_level <- ifelse(
  data$situated_agency_index > median(data$situated_agency_index),
  "higher_agency",
  "lower_agency"
)
data$identity_profile <- paste(data$continuity_level, data$agency_level, sep = "_")
data$high_constraint_low_agency <- data$external_constraint > median(data$external_constraint) &
  data$situated_agency_index < median(data$situated_agency_index)
data$low_continuity_low_integration <- data$temporal_self_continuity < median(data$temporal_self_continuity) &
  data$identity_integration < median(data$identity_integration)

context_summary <- aggregate(
  data[, c("temporal_self_continuity", "agency_index", "situated_agency_index", "social_recognition", "external_constraint", "identity_integration", "well_being")],
  by = list(identity_context = data$identity_context),
  FUN = mean
)
write.csv(context_summary, file.path(outputs, "r_identity_context_summary.csv"), row.names = FALSE)

profile_summary <- aggregate(
  data[, c("temporal_self_continuity", "situated_agency_index", "social_recognition", "external_constraint", "identity_integration", "well_being")],
  by = list(identity_profile = data$identity_profile),
  FUN = mean
)
write.csv(profile_summary, file.path(outputs, "r_identity_profile_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "past_self", "present_self", "future_self", "intentional_clarity", "action_ownership",
  "self_efficacy", "external_constraint", "social_recognition", "value_commitment_gap",
  "identity_integration", "well_being", "past_present_gap", "present_future_gap",
  "temporal_self_continuity", "agency_index", "situated_agency_index", "identity_alignment"
)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_selfhood_agency_identity_correlations.csv"))

model_identity <- lm(
  identity_integration ~ temporal_self_continuity + situated_agency_index +
    social_recognition + external_constraint + value_commitment_gap,
  data = data
)

model_wellbeing <- lm(
  well_being ~ identity_integration + situated_agency_index +
    temporal_self_continuity + social_recognition + external_constraint,
  data = data
)

model_agency <- lm(
  agency_index ~ intentional_clarity + action_ownership + self_efficacy +
    social_recognition + external_constraint,
  data = data
)

capture.output(summary(model_identity), file = file.path(outputs, "r_identity_integration_model_summary.txt"))
capture.output(summary(model_wellbeing), file = file.path(outputs, "r_wellbeing_model_summary.txt"))
capture.output(summary(model_agency), file = file.path(outputs, "r_agency_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_selfhood_agency_identity.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
