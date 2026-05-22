root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_person_situation_data.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

person_cols <- c("trait_score", "trait_extraversion", "trait_conscientiousness", "trait_neuroticism")
state_cols <- c("state_extraversion", "state_conscientiousness", "state_assertiveness", "state_withdrawal")
situation_cols <- c("situation_demand", "situation_sociality", "situation_evaluation", "situation_trust", "situation_autonomy", "situation_threat")

for (v in situation_cols) {
  person_mean <- ave(data[[v]], data$person_id, FUN = mean)
  data[[paste0(v, "_person_mean")]] <- person_mean
  data[[paste0(v, "_within")]] <- data[[v]] - person_mean
}

data <- data[order(data$person_id, data$occasion), ]

for (s in state_cols) {
  data[[paste0("lag_", s)]] <- ave(data[[s]], data$person_id, FUN = function(x) c(NA, x[-length(x)]))
  data[[paste0(s, "_within_deviation")]] <- data[[s]] - ave(data[[s]], data$person_id, FUN = mean)
}

person_summary <- aggregate(
  data[, c(person_cols, state_cols, "behavioral_consistency_marker", "conditional_signature_score", "state_inertia_marker")],
  by = list(person_id = data$person_id, assessment_context = data$assessment_context),
  FUN = mean
)

context_summary <- aggregate(
  data[, c(state_cols, situation_cols, "behavioral_consistency_marker", "conditional_signature_score", "state_inertia_marker")],
  by = list(assessment_context = data$assessment_context),
  FUN = mean
)

icc_rows <- data.frame(
  state = character(),
  between_person_variance = numeric(),
  within_person_variance = numeric(),
  icc_like_ratio = numeric()
)

for (s in state_cols) {
  person_means <- aggregate(data[[s]], by = list(person_id = data$person_id), FUN = mean)
  names(person_means) <- c("person_id", "person_mean")
  merged <- merge(data[, c("person_id", s)], person_means, by = "person_id")
  between <- var(person_means$person_mean)
  within <- var(merged[[s]] - merged$person_mean)
  icc <- between / (between + within)
  icc_rows <- rbind(
    icc_rows,
    data.frame(
      state = s,
      between_person_variance = between,
      within_person_variance = within,
      icc_like_ratio = icc
    )
  )
}

model_extraversion <- lm(
  state_extraversion ~ trait_extraversion +
    situation_sociality_within +
    situation_trust_within +
    situation_autonomy_within,
  data = data
)

model_conscientiousness <- lm(
  state_conscientiousness ~ trait_conscientiousness +
    situation_demand_within +
    situation_evaluation_within +
    situation_autonomy_within,
  data = data
)

model_assertiveness <- lm(
  state_assertiveness ~ trait_score +
    situation_evaluation_within +
    situation_trust_within +
    situation_threat_within,
  data = data
)

model_withdrawal <- lm(
  state_withdrawal ~ trait_neuroticism +
    situation_threat_within +
    situation_evaluation_within +
    situation_trust_within,
  data = data
)

inertia_data <- data[!is.na(data$lag_state_extraversion), ]

model_inertia <- lm(
  state_extraversion ~ lag_state_extraversion +
    situation_sociality_within +
    situation_trust_within,
  data = inertia_data
)

corr_cols <- c(person_cols, state_cols, situation_cols, "behavioral_consistency_marker", "conditional_signature_score", "state_inertia_marker")

write.csv(person_summary, file.path(outputs, "r_person_summary.csv"), row.names = FALSE)
write.csv(context_summary, file.path(outputs, "r_context_summary.csv"), row.names = FALSE)
write.csv(icc_rows, file.path(outputs, "r_icc_like_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_person_situation_correlations.csv"))
capture.output(summary(model_extraversion), file = file.path(outputs, "r_state_extraversion_model_summary.txt"))
capture.output(summary(model_conscientiousness), file = file.path(outputs, "r_state_conscientiousness_model_summary.txt"))
capture.output(summary(model_assertiveness), file = file.path(outputs, "r_state_assertiveness_model_summary.txt"))
capture.output(summary(model_withdrawal), file = file.path(outputs, "r_state_withdrawal_model_summary.txt"))
capture.output(summary(model_inertia), file = file.path(outputs, "r_state_inertia_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_person_situation_data.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
