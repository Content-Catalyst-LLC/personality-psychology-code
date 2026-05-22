root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_narrative_identity.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

data$redemption_level <- ifelse(
  data$redemption > median(data$redemption),
  "higher_redemption",
  "lower_redemption"
)
data$contamination_level <- ifelse(
  data$contamination > median(data$contamination),
  "higher_contamination",
  "lower_contamination"
)
data$coherence_level <- ifelse(
  data$coherence > median(data$coherence),
  "higher_coherence",
  "lower_coherence"
)
data$narrative_profile <- paste(
  data$redemption_level,
  data$contamination_level,
  data$coherence_level,
  sep = "_"
)
data$high_coherence_high_defensiveness <- data$coherence > median(data$coherence) &
  data$defensive_rigidity > median(data$defensive_rigidity)
data$high_contamination_low_continuity <- data$contamination > median(data$contamination) &
  data$self_continuity < median(data$self_continuity)

context_summary <- aggregate(
  data[, c("redemption", "contamination", "coherence", "agency", "communion", "meaning_making", "narrative_flexibility", "defensive_rigidity", "self_continuity", "well_being")],
  by = list(narrative_context = data$narrative_context),
  FUN = mean
)
write.csv(context_summary, file.path(outputs, "r_narrative_context_summary.csv"), row.names = FALSE)

profile_summary <- aggregate(
  data[, c("redemption", "contamination", "coherence", "agency", "meaning_making", "self_continuity", "well_being")],
  by = list(narrative_profile = data$narrative_profile),
  FUN = mean
)
write.csv(profile_summary, file.path(outputs, "r_narrative_profile_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "redemption", "contamination", "coherence", "agency", "communion",
  "meaning_making", "narrative_flexibility", "defensive_rigidity",
  "narrative_growth_orientation", "narrative_burden", "narrative_integration",
  "redemptive_agency_balance", "self_continuity", "well_being"
)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_narrative_identity_correlations.csv"))

model_wellbeing <- lm(
  well_being ~ redemption + contamination + coherence + agency +
    communion + meaning_making + narrative_flexibility,
  data = data
)

model_continuity <- lm(
  self_continuity ~ coherence + redemption + contamination +
    meaning_making + narrative_flexibility + defensive_rigidity,
  data = data
)

model_integration <- lm(
  narrative_integration ~ agency + communion +
    narrative_growth_orientation + narrative_burden,
  data = data
)

capture.output(summary(model_wellbeing), file = file.path(outputs, "r_wellbeing_model_summary.txt"))
capture.output(summary(model_continuity), file = file.path(outputs, "r_self_continuity_model_summary.txt"))
capture.output(summary(model_integration), file = file.path(outputs, "r_narrative_integration_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_narrative_identity.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
