# Personality Disorders and Dimensional Diagnosis
# R workflow for dimensional personality pathology analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_disorders_dimensional_diagnosis.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "participant_id",
  "clinical_context",
  "negative_affectivity",
  "detachment",
  "antagonism",
  "disinhibition",
  "psychoticism",
  "anankastia",
  "identity_impairment",
  "self_direction_impairment",
  "empathy_impairment",
  "intimacy_impairment",
  "self_functioning",
  "interpersonal_functioning",
  "functioning_impairment",
  "maladaptive_trait_burden",
  "severity_trait_interaction",
  "borderline_pattern_indicator",
  "pd_severity",
  "risk_level",
  "treatment_engagement",
  "perceived_support"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

trait_cols <- c(
  "negative_affectivity",
  "detachment",
  "antagonism",
  "disinhibition",
  "psychoticism",
  "anankastia"
)

data$dominant_trait_domain <- trait_cols[
  max.col(data[, trait_cols], ties.method = "first")
]

data$severity_band <- ifelse(
  data$pd_severity < 2.5,
  "lower_severity",
  ifelse(data$pd_severity < 4.5, "moderate_severity", "higher_severity")
)

context_summary <- aggregate(
  data[, c("functioning_impairment", "maladaptive_trait_burden", "pd_severity", "risk_level", "treatment_engagement", "perceived_support")],
  by = list(clinical_context = data$clinical_context),
  FUN = mean
)

context_n <- aggregate(
  data$participant_id,
  by = list(clinical_context = data$clinical_context),
  FUN = length
)
names(context_n)[2] <- "n"
context_summary <- merge(context_n, context_summary, by = "clinical_context")

write.csv(context_summary, file.path(outputs, "r_clinical_context_summary.csv"), row.names = FALSE)

severity_summary <- aggregate(
  data[, c("functioning_impairment", "maladaptive_trait_burden", "negative_affectivity", "detachment", "antagonism", "disinhibition", "psychoticism", "anankastia", "borderline_pattern_indicator", "risk_level")],
  by = list(severity_band = data$severity_band),
  FUN = mean
)

severity_n <- aggregate(
  data$participant_id,
  by = list(severity_band = data$severity_band),
  FUN = length
)
names(severity_n)[2] <- "n"
severity_summary <- merge(severity_n, severity_summary, by = "severity_band")

write.csv(severity_summary, file.path(outputs, "r_severity_band_summary.csv"), row.names = FALSE)

corr_cols <- c(
  trait_cols,
  "identity_impairment",
  "self_direction_impairment",
  "empathy_impairment",
  "intimacy_impairment",
  "self_functioning",
  "interpersonal_functioning",
  "functioning_impairment",
  "maladaptive_trait_burden",
  "severity_trait_interaction",
  "pd_severity",
  "risk_level",
  "treatment_engagement",
  "perceived_support"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_dimensional_pd_correlations.csv"))

model_severity <- lm(
  pd_severity ~ negative_affectivity + detachment + antagonism +
    disinhibition + psychoticism + anankastia +
    functioning_impairment,
  data = data
)

model_interaction <- lm(
  pd_severity ~ functioning_impairment + maladaptive_trait_burden +
    severity_trait_interaction,
  data = data
)

model_risk <- lm(
  risk_level ~ pd_severity + negative_affectivity +
    disinhibition + antagonism + functioning_impairment,
  data = data
)

model_treatment <- lm(
  treatment_engagement ~ pd_severity + functioning_impairment +
    negative_affectivity + detachment + perceived_support,
  data = data
)

capture.output(summary(model_severity), file = file.path(outputs, "r_pd_severity_model_summary.txt"))
capture.output(summary(model_interaction), file = file.path(outputs, "r_severity_trait_interaction_model_summary.txt"))
capture.output(summary(model_risk), file = file.path(outputs, "r_risk_level_model_summary.txt"))
capture.output(summary(model_treatment), file = file.path(outputs, "r_treatment_engagement_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_dimensional_personality_disorders.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
