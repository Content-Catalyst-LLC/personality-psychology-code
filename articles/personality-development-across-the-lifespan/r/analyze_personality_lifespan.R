root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_lifespan.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

traits <- c("neuroticism", "extraversion", "conscientiousness", "openness", "agreeableness")
processes <- c("role_investment", "state_practice_frequency", "perceived_support")

wave_summary <- aggregate(
  data[, c(traits, processes)],
  by = list(wave = data$wave, wave_numeric = data$wave_numeric),
  FUN = mean
)
write.csv(wave_summary, file.path(outputs, "r_wave_summary.csv"), row.names = FALSE)

life_stage_summary <- aggregate(
  data[, c("age", traits, processes)],
  by = list(life_stage = data$life_stage),
  FUN = mean
)
write.csv(life_stage_summary, file.path(outputs, "r_life_stage_summary.csv"), row.names = FALSE)

cohort_culture_summary <- aggregate(
  data[, c(traits, processes)],
  by = list(cohort = data$cohort, cultural_context = data$cultural_context),
  FUN = mean
)
write.csv(cohort_culture_summary, file.path(outputs, "r_cohort_culture_summary.csv"), row.names = FALSE)

people <- unique(data$person_id)
change_rows <- list()
wide_rows <- list()

for (person in people) {
  person_data <- data[data$person_id == person, ]
  person_data <- person_data[order(person_data$wave_numeric), ]
  first_row <- person_data[1, ]
  last_row <- person_data[nrow(person_data), ]
  row <- data.frame(
    person_id = person,
    cohort = first_row$cohort,
    cultural_context = first_row$cultural_context,
    age_first = first_row$age,
    age_last = last_row$age,
    role_investment_mean = mean(person_data$role_investment),
    state_practice_mean = mean(person_data$state_practice_frequency),
    perceived_support_mean = mean(person_data$perceived_support)
  )
  wide <- data.frame(person_id = person, cohort = first_row$cohort, cultural_context = first_row$cultural_context)
  for (trait in traits) {
    row[[paste0(trait, "_change")]] <- last_row[[trait]] - first_row[[trait]]
    wide[[paste0(trait, "_first")]] <- first_row[[trait]]
    wide[[paste0(trait, "_last")]] <- last_row[[trait]]
  }
  change_rows[[length(change_rows) + 1]] <- row
  wide_rows[[length(wide_rows) + 1]] <- wide
}

change_summary <- do.call(rbind, change_rows)
wide_traits <- do.call(rbind, wide_rows)

rank_order_stability <- data.frame(
  trait = traits,
  rank_order_stability_first_last = sapply(traits, function(trait) {
    cor(wide_traits[[paste0(trait, "_first")]], wide_traits[[paste0(trait, "_last")]], use = "pairwise.complete.obs")
  }),
  mean_level_change_first_last = sapply(traits, function(trait) {
    mean(wide_traits[[paste0(trait, "_last")]]) - mean(wide_traits[[paste0(trait, "_first")]])
  })
)

write.csv(change_summary, file.path(outputs, "r_individual_change_summary.csv"), row.names = FALSE)
write.csv(rank_order_stability, file.path(outputs, "r_rank_order_stability.csv"), row.names = FALSE)

data$cohort <- as.factor(data$cohort)
data$cultural_context <- as.factor(data$cultural_context)

model_conscientiousness <- lm(
  conscientiousness ~ age + role_investment + state_practice_frequency +
    perceived_support + cohort + cultural_context,
  data = data
)

model_neuroticism <- lm(
  neuroticism ~ age + role_investment + state_practice_frequency +
    perceived_support + cohort + cultural_context,
  data = data
)

model_openness <- lm(
  openness ~ age + role_investment + state_practice_frequency +
    perceived_support + cohort + cultural_context,
  data = data
)

capture.output(summary(model_conscientiousness), file = file.path(outputs, "r_conscientiousness_model_summary.txt"))
capture.output(summary(model_neuroticism), file = file.path(outputs, "r_neuroticism_model_summary.txt"))
capture.output(summary(model_openness), file = file.path(outputs, "r_openness_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_personality_lifespan.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
