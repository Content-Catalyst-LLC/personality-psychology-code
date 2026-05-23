DROP TABLE IF EXISTS personality_summary;

CREATE TABLE personality_summary (
    person_id TEXT PRIMARY KEY,
    conscientiousness_score REAL,
    extraversion_score REAL,
    neuroticism_score REAL,
    identity_coherence REAL,
    life_satisfaction REAL,
    social_functioning REAL,
    developmental_integration REAL,
    measurement_reliability_index REAL,
    identity_trait_alignment_index REAL,
    person_situation_sensitivity_index REAL,
    responsible_interpretation_index REAL,
    mean_behavior_score REAL,
    mean_situation_strength REAL,
    mean_observed_regulation REAL,
    mean_contextual_constraint REAL
);

.mode csv
.import --skip 1 data/synthetic_personality_summary_for_sql.csv personality_summary

.headers on
.mode column

SELECT
  ROUND(AVG(conscientiousness_score),3) AS conscientiousness_mean,
  ROUND(AVG(extraversion_score),3) AS extraversion_mean,
  ROUND(AVG(neuroticism_score),3) AS neuroticism_mean,
  ROUND(AVG(identity_coherence),3) AS identity_coherence_mean,
  ROUND(AVG(life_satisfaction),3) AS life_satisfaction_mean,
  ROUND(AVG(responsible_interpretation_index),3) AS responsible_interpretation_mean
FROM personality_summary;

SELECT person_id,
       conscientiousness_score,
       extraversion_score,
       neuroticism_score,
       identity_coherence,
       life_satisfaction,
       mean_behavior_score,
       responsible_interpretation_index
FROM personality_summary
ORDER BY responsible_interpretation_index DESC
LIMIT 25;
