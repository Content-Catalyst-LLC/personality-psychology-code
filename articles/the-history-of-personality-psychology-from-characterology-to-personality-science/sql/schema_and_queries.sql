DROP TABLE IF EXISTS personality_history;

CREATE TABLE personality_history (
    participant_id TEXT PRIMARY KEY,
    extraversion_score REAL,
    agreeableness_score REAL,
    conscientiousness_score REAL,
    neuroticism_score REAL,
    openness_score REAL,
    conscientiousness_t1 REAL,
    conscientiousness_t2 REAL,
    behavior_score REAL,
    trait_score REAL,
    situation_strength REAL,
    person_situation_interaction REAL,
    characterology_typology_index REAL,
    psychometric_structure_index REAL,
    person_situation_index REAL,
    narrative_identity_index REAL,
    measurement_invariance_caution_index REAL,
    historical_method_maturity_index REAL
);

.mode csv
.import --skip 1 data/synthetic_personality_history_scores_for_sql.csv personality_history

.headers on
.mode column

SELECT
  ROUND(AVG(characterology_typology_index),3) AS typology_residual_mean,
  ROUND(AVG(psychometric_structure_index),3) AS psychometric_structure_mean,
  ROUND(AVG(person_situation_index),3) AS person_situation_mean,
  ROUND(AVG(narrative_identity_index),3) AS narrative_identity_mean,
  ROUND(AVG(measurement_invariance_caution_index),3) AS invariance_caution_mean,
  ROUND(AVG(historical_method_maturity_index),3) AS method_maturity_mean
FROM personality_history;

SELECT participant_id,
       conscientiousness_t1,
       conscientiousness_t2,
       ROUND(conscientiousness_t2 - conscientiousness_t1, 3) AS change_score,
       behavior_score,
       trait_score,
       situation_strength,
       historical_method_maturity_index
FROM personality_history
ORDER BY historical_method_maturity_index DESC
LIMIT 25;
