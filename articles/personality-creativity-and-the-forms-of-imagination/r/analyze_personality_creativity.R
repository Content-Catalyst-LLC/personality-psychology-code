#!/usr/bin/env Rscript

# Analyze synthetic personality-creativity data.
# Companion workflow for "Personality, Creativity, and the Forms of Imagination."

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
  library(broom)
})

`%||%` <- function(x, y) if (is.null(x)) y else x

script_path <- normalizePath(sys.frames()[[1]]$ofile %||% "r/analyze_personality_creativity.R", mustWork = FALSE)
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)

data_path <- file.path(article_dir, "data", "synthetic_personality_creativity.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
figure_dir <- file.path(article_dir, "outputs", "figures")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figure_dir, recursive = TRUE, showWarnings = FALSE)

data <- read_csv(data_path, show_col_types = FALSE)

numeric_vars <- c(
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

descriptive <- data %>%
  summarise(across(all_of(numeric_vars), list(mean = mean, sd = sd), na.rm = TRUE))

write_csv(descriptive, file.path(table_dir, "r_descriptive_statistics.csv"))

cor_matrix <- cor(data[, numeric_vars], use = "pairwise.complete.obs")
write_csv(as.data.frame(cor_matrix), file.path(table_dir, "r_correlation_matrix.csv"))

model_dt <- lm(
  divergent_thinking ~ openness + intellect + conscientiousness +
    extraversion + agreeableness + neuroticism,
  data = data
)

model_ca <- lm(
  creative_achievement ~ openness + intellect + conscientiousness +
    persistence + social_support + domain,
  data = data
)

model_ec <- lm(
  everyday_creativity ~ openness + intellect + conscientiousness +
    extraversion + agreeableness + persistence + social_support + domain,
  data = data
)

model_results <- bind_rows(
  tidy(model_dt) %>% mutate(model = "divergent_thinking"),
  tidy(model_ca) %>% mutate(model = "creative_achievement"),
  tidy(model_ec) %>% mutate(model = "everyday_creativity")
) %>%
  select(model, term, estimate, std.error, statistic, p.value)

write_csv(model_results, file.path(table_dir, "r_model_coefficients.csv"))

plot_dt <- ggplot(data, aes(x = openness, y = divergent_thinking)) +
  geom_point(alpha = 0.75) +
  geom_smooth(method = "lm", se = TRUE) +
  labs(
    title = "Openness and Divergent Thinking",
    x = "Openness",
    y = "Divergent Thinking"
  )

ggsave(
  filename = file.path(figure_dir, "r_openness_divergent_thinking.png"),
  plot = plot_dt,
  width = 7,
  height = 5,
  dpi = 300
)

plot_ca <- ggplot(data, aes(x = openness, y = creative_achievement)) +
  geom_point(alpha = 0.75) +
  geom_smooth(method = "lm", se = TRUE) +
  labs(
    title = "Openness and Creative Achievement",
    x = "Openness",
    y = "Creative Achievement"
  )

ggsave(
  filename = file.path(figure_dir, "r_openness_creative_achievement.png"),
  plot = plot_ca,
  width = 7,
  height = 5,
  dpi = 300
)

cat("R analysis complete.\n")
cat("Tables written to:", table_dir, "\n")
cat("Figures written to:", figure_dir, "\n")
