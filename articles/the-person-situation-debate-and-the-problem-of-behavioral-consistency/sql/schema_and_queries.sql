DROP TABLE IF EXISTS person_situation_debate;

CREATE TABLE person_situation_debate (
    person_id TEXT NOT NULL,
    assessment_context TEXT NOT NULL,
    occasion INTEGER NOT NULL,
    trait_score REAL,
    trait_extraversion REAL,
    trait_conscientiousness REAL,
    trait_neuroticism REAL,
    state_extraversion REAL,
    state_conscientiousness REAL,
    state_assertiveness REAL,
    state_withdrawal REAL,
    situation_demand REAL,
    situation_sociality REAL,
    situation_evaluation REAL,
    situation_trust REAL,
    situation_autonomy REAL,
    situation_threat REAL,
    behavioral_consistency_marker REAL,
    conditional_signature_score REAL,
    state_inertia_marker REAL
);

.mode csv
.import --skip 1 data/synthetic_person_situation_data.csv person_situation_debate

.headers on
.mode column

SELECT assessment_context,
       COUNT(DISTINCT person_id) AS n_persons,
       COUNT(*) AS n_observations,
       ROUND(AVG(state_extraversion),3) AS state_extraversion_mean,
       ROUND(AVG(state_conscientiousness),3) AS state_conscientiousness_mean,
       ROUND(AVG(state_assertiveness),3) AS state_assertiveness_mean,
       ROUND(AVG(state_withdrawal),3) AS state_withdrawal_mean,
       ROUND(AVG(situation_demand),3) AS demand_mean,
       ROUND(AVG(situation_sociality),3) AS sociality_mean,
       ROUND(AVG(situation_threat),3) AS threat_mean,
       ROUND(AVG(conditional_signature_score),3) AS conditional_signature_mean,
       ROUND(AVG(behavioral_consistency_marker),3) AS consistency_marker_mean
FROM person_situation_debate
GROUP BY assessment_context
ORDER BY conditional_signature_mean DESC;

SELECT person_id,
       COUNT(*) AS n_obs,
       ROUND(AVG(state_extraversion),3) AS mean_state_extraversion,
       ROUND(AVG(state_conscientiousness),3) AS mean_state_conscientiousness,
       ROUND(AVG(state_assertiveness),3) AS mean_state_assertiveness,
       ROUND(AVG(state_withdrawal),3) AS mean_state_withdrawal,
       ROUND(AVG(conditional_signature_score),3) AS mean_conditional_signature
FROM person_situation_debate
GROUP BY person_id
ORDER BY mean_conditional_signature DESC
LIMIT 25;
