#!/usr/bin/env Rscript

# Analyze synthetic personality-creativity data using base R.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(root, "data", "synthetic_personality_creativity.csv")
table_dir <- file.path(root, "outputs", "tables")
figure_dir <- file.path(root, "outputs", "figures")
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figure_dir, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(data_path)

numeric_cols <- c(
  "openness",
  "intellect",
  "conscientiousness",
  "extraversion",
  "agreeableness",
  "neuroticism",
  "persistence",
  "social_support",
  "divergent_thinking",
  "creative_achievement",
  "everyday_creativity"
)

write.csv(summary(df[numeric_cols]), file.path(table_dir, "r_descriptive_summary.csv"))
write.csv(round(cor(df[numeric_cols], use = "pairwise.complete.obs"), 3), file.path(table_dir, "r_correlation_matrix.csv"))

domain_means <- aggregate(df[c("divergent_thinking", "creative_achievement", "everyday_creativity")], by = list(domain = df$domain), mean)
write.csv(domain_means, file.path(table_dir, "r_domain_outcome_means.csv"), row.names = FALSE)

model_dt <- lm(divergent_thinking ~ openness + intellect + conscientiousness + persistence + social_support, data = df)
model_ca <- lm(creative_achievement ~ openness + intellect + conscientiousness + persistence + social_support, data = df)
model_domain <- lm(creative_achievement ~ openness * domain + intellect * domain + persistence + social_support, data = df)

capture.output(summary(model_dt), file = file.path(table_dir, "r_model_divergent_thinking.txt"))
capture.output(summary(model_ca), file = file.path(table_dir, "r_model_creative_achievement.txt"))
capture.output(summary(model_domain), file = file.path(table_dir, "r_model_domain_sensitive.txt"))

png(file.path(figure_dir, "r_openness_creative_achievement.png"), width = 900, height = 650)
plot(df$openness, df$creative_achievement,
     xlab = "Openness", ylab = "Creative Achievement",
     main = "Openness and Creative Achievement")
abline(lm(creative_achievement ~ openness, data = df))
dev.off()

cat("R analysis complete. Outputs written to:", table_dir, "and", figure_dir, "\n")
