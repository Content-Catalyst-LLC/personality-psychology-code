# Personality, Culture, and the Problem of Universality
# R workflow for synthetic cross-cultural personality analysis

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_culture_universality.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

traits <- c(
  "openness",
  "conscientiousness",
  "extraversion",
  "agreeableness",
  "neuroticism",
  "honesty_humility"
)

required <- c("participant_id", "culture_group", traits, "context_collectivism", "behavioral_manifestation")
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

group_summary <- aggregate(
  data[, c(traits, "context_collectivism", "behavioral_manifestation")],
  by = list(culture_group = data$culture_group),
  FUN = mean
)

group_n <- aggregate(
  data$participant_id,
  by = list(culture_group = data$culture_group),
  FUN = length
)
names(group_n)[2] <- "n"

group_summary <- merge(group_n, group_summary, by = "culture_group")
write.csv(group_summary, file.path(outputs, "r_group_summary.csv"), row.names = FALSE)

pooled_corr <- cor(data[, traits], use = "pairwise.complete.obs")
write.csv(pooled_corr, file.path(outputs, "r_pooled_trait_correlations.csv"))

upper_values <- function(mat) {
  mat[upper.tri(mat)]
}

pooled_values <- upper_values(pooled_corr)

rows <- data.frame(
  culture_group = character(),
  matrix_similarity_with_pooled = numeric(),
  n = integer()
)

for (group_name in unique(data$culture_group)) {
  group_df <- data[data$culture_group == group_name, ]
  group_corr <- cor(group_df[, traits], use = "pairwise.complete.obs")
  write.csv(group_corr, file.path(outputs, paste0("r_correlations_", group_name, ".csv")))

  similarity <- cor(pooled_values, upper_values(group_corr), use = "complete.obs")
  rows <- rbind(rows, data.frame(
    culture_group = group_name,
    matrix_similarity_with_pooled = round(similarity, 4),
    n = nrow(group_df)
  ))
}

write.csv(rows, file.path(outputs, "r_matrix_similarity.csv"), row.names = FALSE)

model <- lm(
  behavioral_manifestation ~ conscientiousness + agreeableness + honesty_humility + context_collectivism,
  data = data
)

capture.output(summary(model), file = file.path(outputs, "r_behavioral_model_summary.txt"))

cat("Wrote R outputs to:", outputs, "\n")
