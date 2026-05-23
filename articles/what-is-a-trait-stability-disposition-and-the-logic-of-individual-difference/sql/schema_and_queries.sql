DROP TABLE IF EXISTS trait_state_summary;

CREATE TABLE trait_state_summary (
    person_id TEXT PRIMARY KEY,
    conscientiousness_score REAL,
    extraversion_score REAL,
    neuroticism_score REAL,
    mean_state_conscientiousness REAL,
    sd_state_conscientiousness REAL,
    mean_state_extraversion REAL,
    sd_state_extraversion REAL,
    mean_state_neuroticism REAL,
    sd_state_neuroticism REAL,
    n_observations INTEGER,
    trait_state_alignment_index REAL,
    state_variability_index REAL,
    person_situation_sensitivity_index REAL,
    aggregation_reliability_index REAL
);

.mode csv
.import --skip 1 data/synthetic_trait_state_summary_for_sql.csv trait_state_summary

.headers on
.mode column

SELECT
  ROUND(AVG(conscientiousness_score),3) AS conscientiousness_mean,
  ROUND(AVG(extraversion_score),3) AS extraversion_mean,
  ROUND(AVG(neuroticism_score),3) AS neuroticism_mean,
  ROUND(AVG(trait_state_alignment_index),3) AS trait_state_alignment_mean,
  ROUND(AVG(state_variability_index),3) AS state_variability_mean,
  ROUND(AVG(aggregation_reliability_index),3) AS aggregation_reliability_mean
FROM trait_state_summary;

SELECT person_id,
       conscientiousness_score,
       mean_state_conscientiousness,
       sd_state_conscientiousness,
       trait_state_alignment_index,
       state_variability_index,
       aggregation_reliability_index
FROM trait_state_summary
ORDER BY trait_state_alignment_index DESC
LIMIT 25;
