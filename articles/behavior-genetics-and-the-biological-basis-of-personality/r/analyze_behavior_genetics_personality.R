root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "synthetic_personality_twin_data.csv")
outputs <- file.path(root, "outputs")
dir.create(outputs, showWarnings = FALSE, recursive = TRUE)

data <- read.csv(data_path, stringsAsFactors = FALSE)

twin_corr <- function(df, col1, col2) {
  cor(df[[col1]], df[[col2]], use = "pairwise.complete.obs")
}

rough_ace <- function(r_mz, r_dz) {
  data.frame(
    component = c("additive_genetic_h2", "shared_environment_c2", "nonshared_environment_e2"),
    estimate = c(2 * (r_mz - r_dz), 2 * r_dz - r_mz, 1 - r_mz)
  )
}

outcomes <- list(
  personality_trait = c("twin1_trait", "twin2_trait"),
  temperament_reactivity = c("twin1_temperament_reactivity", "twin2_temperament_reactivity"),
  effortful_control = c("twin1_effortful_control", "twin2_effortful_control")
)

correlation_rows <- data.frame()
ace_rows <- data.frame()

for (name in names(outcomes)) {
  cols <- outcomes[[name]]
  mz <- data[data$zygosity == "MZ", ]
  dz <- data[data$zygosity == "DZ", ]
  r_mz <- twin_corr(mz, cols[1], cols[2])
  r_dz <- twin_corr(dz, cols[1], cols[2])

  correlation_rows <- rbind(
    correlation_rows,
    data.frame(outcome = name, zygosity = "MZ", n_pairs = nrow(mz), twin_correlation = r_mz),
    data.frame(outcome = name, zygosity = "DZ", n_pairs = nrow(dz), twin_correlation = r_dz)
  )

  ace <- rough_ace(r_mz, r_dz)
  ace$outcome <- name
  ace$r_mz <- r_mz
  ace$r_dz <- r_dz
  ace_rows <- rbind(ace_rows, ace)
}

set.seed(20260522)
boot_rows <- data.frame()
for (i in 1:500) {
  mz_sample <- data[data$zygosity == "MZ", ][sample(which(data$zygosity == "MZ"), replace = TRUE), ]
  dz_sample <- data[data$zygosity == "DZ", ][sample(which(data$zygosity == "DZ"), replace = TRUE), ]

  r_mz <- twin_corr(mz_sample, "twin1_trait", "twin2_trait")
  r_dz <- twin_corr(dz_sample, "twin1_trait", "twin2_trait")
  ace <- rough_ace(r_mz, r_dz)

  boot_rows <- rbind(
    boot_rows,
    data.frame(
      replicate = i,
      additive_genetic_h2 = ace$estimate[ace$component == "additive_genetic_h2"],
      shared_environment_c2 = ace$estimate[ace$component == "shared_environment_c2"],
      nonshared_environment_e2 = ace$estimate[ace$component == "nonshared_environment_e2"]
    )
  )
}

boot_summary <- data.frame(
  component = c("additive_genetic_h2", "shared_environment_c2", "nonshared_environment_e2"),
  mean = c(mean(boot_rows$additive_genetic_h2), mean(boot_rows$shared_environment_c2), mean(boot_rows$nonshared_environment_e2)),
  lower_95 = c(quantile(boot_rows$additive_genetic_h2, 0.025), quantile(boot_rows$shared_environment_c2, 0.025), quantile(boot_rows$nonshared_environment_e2, 0.025)),
  upper_95 = c(quantile(boot_rows$additive_genetic_h2, 0.975), quantile(boot_rows$shared_environment_c2, 0.975), quantile(boot_rows$nonshared_environment_e2, 0.975))
)

data$zygosity_mz <- ifelse(data$zygosity == "MZ", 1, 0)
data$family_stress_centered <- data$family_stress - mean(data$family_stress)
data$social_support_centered <- data$social_support - mean(data$social_support)
data$socioeconomic_security_centered <- data$socioeconomic_security - mean(data$socioeconomic_security)
data$educational_stability_centered <- data$educational_stability - mean(data$educational_stability)

model_difference <- lm(
  trait_difference ~ zygosity_mz + family_stress_centered +
    social_support_centered + socioeconomic_security_centered +
    nonshared_environment_index,
  data = data
)

model_gxe <- lm(
  gxe_marker ~ genetic_relatedness + family_stress_centered +
    social_support_centered + educational_stability_centered,
  data = data
)

model_rge <- lm(
  rge_marker ~ trait_mean + social_support_centered +
    socioeconomic_security_centered + developmental_context_score,
  data = data
)

pair_summary <- aggregate(
  data[, c("trait_mean", "trait_difference", "family_stress", "social_support", "socioeconomic_security", "nonshared_environment_index", "gxe_marker", "rge_marker", "developmental_context_score")],
  by = list(zygosity = data$zygosity),
  FUN = mean
)

corr_cols <- c(
  "genetic_relatedness",
  "twin1_trait",
  "twin2_trait",
  "trait_mean",
  "trait_difference",
  "family_stress",
  "social_support",
  "socioeconomic_security",
  "educational_stability",
  "shared_environment_index",
  "nonshared_environment_index",
  "gxe_marker",
  "rge_marker",
  "developmental_context_score"
)

write.csv(correlation_rows, file.path(outputs, "r_twin_correlations.csv"), row.names = FALSE)
write.csv(ace_rows, file.path(outputs, "r_rough_ace_summary.csv"), row.names = FALSE)
write.csv(boot_rows, file.path(outputs, "r_ace_bootstrap.csv"), row.names = FALSE)
write.csv(boot_summary, file.path(outputs, "r_ace_bootstrap_summary.csv"), row.names = FALSE)
write.csv(pair_summary, file.path(outputs, "r_pair_summary.csv"), row.names = FALSE)
write.csv(cor(data[, corr_cols], use = "pairwise.complete.obs"), file.path(outputs, "r_behavior_genetics_correlations.csv"))
capture.output(summary(model_difference), file = file.path(outputs, "r_trait_difference_model_summary.txt"))
capture.output(summary(model_gxe), file = file.path(outputs, "r_gxe_marker_model_summary.txt"))
capture.output(summary(model_rge), file = file.path(outputs, "r_rge_marker_model_summary.txt"))
write.csv(data, file.path(outputs, "r_scored_personality_twin_data.csv"), row.names = FALSE)
cat("Wrote R outputs to:", outputs, "\n")
