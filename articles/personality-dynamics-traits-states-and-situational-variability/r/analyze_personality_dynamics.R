root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_dynamics_data.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

traits <- c("trait_extraversion", "trait_conscientiousness", "trait_neuroticism")
states <- c("state_extraversion", "state_conscientiousness", "state_neuroticism")
situations <- c("situation_valence", "situation_sociality", "situation_demand", "situation_evaluation")

# Within-person centered situation variables.
for (v in situations) {
  person_mean <- ave(data[[v]], data$person_id, FUN = mean)
  data[[paste0(v, "_person_mean")]] <- person_mean
  data[[paste0(v, "_within")]] <- data[[v]] - person_mean
}

data <- data[order(data$person_id, data$occasion), ]

for (s in states) {
  data[[paste0("lag_", s)]] <- ave(data[[s]], data$person_id, FUN = function(x) c(NA, x[-length(x)]))
  data[[paste0(s, "_within_deviation")]] <- data[[s]] - ave(data[[s]], data$person_id, FUN = mean)
}

person_summary <- aggregate(
  data[, c(traits, states, "positive_affect", "negative_affect", "state_inertia_marker", "dynamic_signature_score")],
  by = list(person_id = data$person_id, assessment_context = data$assessment_context),
  FUN = mean
)

context_summary <- aggregate(
  data[, c(states, situations, "positive_affect", "negative_affect", "goal_pressure", "autonomy_support", "dynamic_signature_score")],
  by = list(assessment_context = data$assessment_context),
  FUN = mean
)

icc_rows <- data.frame(
  state = character(),
  between_person_variance = numeric(),
  within_person_variance = numeric(),
  icc_like_ratio = numeric()
)

for (s in states) {
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
    situation_valence_within +
    autonomy_support,
  data = data
)

model_conscientiousness <- lm(
  state_conscientiousness ~ trait_conscientiousness +
    situation_demand_within +
    goal_pressure +
    autonomy_support,
  data = data
)

model_neuroticism <- lm(
  state_neuroticism ~ trait_neuroticism +
    situation_evaluation_within +
    situation_valence_within +
    negative_affect,
  data = data
)

inertia_data <- data[!is.na(data$lag_state_extraversion), ]

model_inertia <- lm(
  state_extraversion ~ lag_state_extraversion +
    situation_sociality_within +
    positive_affect,
  data = inertia_data
)

corr_cols <- c(
  traits,
  states,
  situations,
  "positive_affect",
  "negative_affect",
  "goal_pressure",
  "autonomy_support",
  "state_inertia_marker",
  "dynamic_signature_score"
)

write.csv(person_summary, file.path(outputs, "r_person_summary.csv"), row.names = FALSE)
write.csv(context_summary, file.path(outputs, "r_context_summary.csv"), row.names = FALSE)
write.csv(icc_rows, file.path(outputs, "r_icc_like_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_dynamic_correlations.csv"))
capture.output(summary(model_extraversion), file = file.path(outputs, "r_state_extraversion_model_summary.txt"))
capture.output(summary(model_conscientiousness), file = file.path(outputs, "r_state_conscientiousness_model_summary.txt"))
capture.output(summary(model_neuroticism), file = file.path(outputs, "r_state_neuroticism_model_summary.txt"))
capture.output(summary(model_inertia), file = file.path(outputs, "r_state_inertia_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_personality_dynamics_data.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
