# Synthetic personality psychology analysis.
# Run after the Python script creates data/processed/synthetic_personality_outcomes.csv.

data_path <- file.path("data", "processed", "synthetic_personality_outcomes.csv")

if (!file.exists(data_path)) {
  stop("Run: python3 python/personality_simulation.py")
}

dat <- read.csv(data_path)

summary_table <- aggregate(
  cbind(personality_organization, identity_integration, self_regulation,
        adaptive_flexibility, maladaptive_pressure) ~ period,
  data = dat,
  FUN = mean
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_table, file.path("outputs", "personality_period_summary.csv"), row.names = FALSE)

model <- lm(
  personality_organization ~ identity_integration + self_regulation +
    adaptive_flexibility - maladaptive_pressure,
  data = dat
)

print(summary(model))
print(summary_table)
