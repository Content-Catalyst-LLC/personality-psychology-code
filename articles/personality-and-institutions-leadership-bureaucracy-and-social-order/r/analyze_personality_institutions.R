# Personality and Institutions: Leadership, Bureaucracy, and Social Order
# R workflow for institutional-personality analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_institutions_bureaucracy.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

required <- c(
  "participant_id",
  "institutional_unit",
  "role_type",
  "conscientiousness",
  "agreeableness",
  "emotional_stability",
  "openness",
  "dark_trait_pressure",
  "bureaucratic_fit",
  "discretion_level",
  "accountability_strength",
  "leadership_rating",
  "institutional_performance",
  "institutional_trust",
  "role_clarity"
)

missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

data$role_fit_index <- (
  data$bureaucratic_fit +
  data$conscientiousness +
  data$accountability_strength +
  data$role_clarity
) / 4

data$institutional_risk_index <- (
  data$dark_trait_pressure +
  data$discretion_level -
  data$accountability_strength -
  data$role_clarity
)

data$stewardship_index <- (
  data$conscientiousness +
  data$agreeableness +
  data$emotional_stability +
  data$bureaucratic_fit +
  data$accountability_strength -
  data$dark_trait_pressure
) / 5

unit_summary <- aggregate(
  data[, c("role_fit_index", "institutional_risk_index", "stewardship_index", "institutional_performance", "institutional_trust")],
  by = list(institutional_unit = data$institutional_unit),
  FUN = mean
)

unit_n <- aggregate(
  data$participant_id,
  by = list(institutional_unit = data$institutional_unit),
  FUN = length
)
names(unit_n)[2] <- "n"
unit_summary <- merge(unit_n, unit_summary, by = "institutional_unit")

write.csv(unit_summary, file.path(outputs, "r_institutional_unit_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "conscientiousness",
  "agreeableness",
  "emotional_stability",
  "openness",
  "dark_trait_pressure",
  "bureaucratic_fit",
  "discretion_level",
  "accountability_strength",
  "role_clarity",
  "role_fit_index",
  "institutional_risk_index",
  "stewardship_index",
  "leadership_rating",
  "institutional_performance",
  "institutional_trust"
)

cor_matrix <- cor(data[, corr_cols], use = "pairwise.complete.obs")
write.csv(cor_matrix, file.path(outputs, "r_trait_institution_correlations.csv"))

model_lead <- lm(
  leadership_rating ~ conscientiousness + agreeableness + emotional_stability +
    openness + dark_trait_pressure + bureaucratic_fit + discretion_level +
    accountability_strength + role_clarity,
  data = data
)

model_perf <- lm(
  institutional_performance ~ conscientiousness + agreeableness + emotional_stability +
    openness + dark_trait_pressure + bureaucratic_fit + discretion_level +
    accountability_strength + role_clarity,
  data = data
)

model_trust <- lm(
  institutional_trust ~ conscientiousness + agreeableness + emotional_stability +
    openness + dark_trait_pressure + bureaucratic_fit + discretion_level *
    accountability_strength + role_clarity,
  data = data
)

capture.output(summary(model_lead), file = file.path(outputs, "r_leadership_model_summary.txt"))
capture.output(summary(model_perf), file = file.path(outputs, "r_performance_model_summary.txt"))
capture.output(summary(model_trust), file = file.path(outputs, "r_trust_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_institutions.csv"), row.names = FALSE)

cat("Wrote R outputs to:", outputs, "\n")
