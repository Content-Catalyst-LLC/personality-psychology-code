root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_maladaptive_personality_structure.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)
trait_cols <- c("negative_affectivity", "detachment", "antagonism", "disinhibition", "psychoticism", "anankastia")
data$dominant_trait_domain <- trait_cols[max.col(data[, trait_cols], ties.method = "first")]
data$severity_band <- ifelse(data$clinical_severity < 2.5, "lower_severity", ifelse(data$clinical_severity < 4.5, "moderate_severity", "higher_severity"))

context_summary <- aggregate(
  data[, c("functioning_impairment", "maladaptive_trait_burden", "rigidity", "pervasiveness", "clinical_severity", "clinical_liability")],
  by = list(clinical_context = data$clinical_context),
  FUN = mean
)
write.csv(context_summary, file.path(outputs, "r_clinical_context_summary.csv"), row.names = FALSE)

severity_summary <- aggregate(
  data[, c("functioning_impairment", "maladaptive_trait_burden", "rigidity", "pervasiveness", "threshold_zone_indicator")],
  by = list(severity_band = data$severity_band),
  FUN = mean
)
write.csv(severity_summary, file.path(outputs, "r_severity_band_summary.csv"), row.names = FALSE)

corr_cols <- c(trait_cols, "identity_impairment", "self_direction_impairment", "empathy_impairment", "intimacy_impairment", "functioning_impairment", "maladaptive_trait_burden", "clinical_severity", "clinical_liability", "threshold_zone_indicator", "rigidity", "pervasiveness", "contextual_stress", "perceived_support")
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_maladaptive_personality_correlations.csv"))

model_severity <- lm(clinical_severity ~ negative_affectivity + detachment + antagonism + disinhibition + psychoticism + anankastia + functioning_impairment, data = data)
model_liability <- lm(clinical_liability ~ maladaptive_trait_burden + functioning_impairment + rigidity + pervasiveness + contextual_stress + perceived_support, data = data)

capture.output(summary(model_severity), file = file.path(outputs, "r_clinical_severity_model_summary.txt"))
capture.output(summary(model_liability), file = file.path(outputs, "r_clinical_liability_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_maladaptive_personality.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
