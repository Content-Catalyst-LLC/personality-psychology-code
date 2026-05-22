root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_psychodynamic_personality.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

data$defense_profile <- ifelse(
  data$mature_defenses > data$immature_defenses & data$mature_defenses > data$neurotic_defenses,
  "mature_defense_dominant",
  ifelse(
    data$immature_defenses > data$mature_defenses & data$immature_defenses > data$neurotic_defenses,
    "immature_defense_dominant",
    ifelse(
      data$neurotic_defenses > data$mature_defenses & data$neurotic_defenses > data$immature_defenses,
      "neurotic_defense_dominant",
      "mixed_defensive_profile"
    )
  )
)

context_summary <- aggregate(
  data[, c("mature_defenses", "immature_defenses", "defensive_rigidity", "attachment_insecurity", "self_relational_capacity", "character_integration", "symptom_distress")],
  by = list(developmental_context = data$developmental_context),
  FUN = mean
)
write.csv(context_summary, file.path(outputs, "r_developmental_context_summary.csv"), row.names = FALSE)

profile_summary <- aggregate(
  data[, c("defensive_maturity", "attachment_insecurity", "self_relational_capacity", "character_integration", "symptom_distress")],
  by = list(defense_profile = data$defense_profile),
  FUN = mean
)
write.csv(profile_summary, file.path(outputs, "r_defense_profile_summary.csv"), row.names = FALSE)

corr_cols <- c(
  "mature_defenses", "neurotic_defenses", "immature_defenses", "defensive_rigidity",
  "attachment_anxiety", "attachment_avoidance", "self_cohesion", "relational_security",
  "reflective_functioning", "defensive_maturity", "attachment_insecurity",
  "self_relational_capacity", "hidden_structure_risk", "character_integration", "symptom_distress"
)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_psychodynamic_correlations.csv"))

model_character <- lm(
  character_integration ~ mature_defenses + neurotic_defenses + immature_defenses +
    defensive_rigidity + attachment_anxiety + attachment_avoidance + reflective_functioning,
  data = data
)

model_self_relation <- lm(
  self_relational_capacity ~ defensive_maturity + attachment_insecurity + reflective_functioning,
  data = data
)

model_distress <- lm(
  symptom_distress ~ hidden_structure_risk + character_integration + self_relational_capacity,
  data = data
)

capture.output(summary(model_character), file = file.path(outputs, "r_character_integration_model_summary.txt"))
capture.output(summary(model_self_relation), file = file.path(outputs, "r_self_relational_capacity_model_summary.txt"))
capture.output(summary(model_distress), file = file.path(outputs, "r_symptom_distress_model_summary.txt"))

write.csv(data, file.path(outputs, "r_scored_psychodynamic_personality.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
