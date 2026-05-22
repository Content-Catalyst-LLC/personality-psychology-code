DROP TABLE IF EXISTS personality_dynamics;

CREATE TABLE personality_dynamics (
    person_id TEXT NOT NULL,
    assessment_context TEXT NOT NULL,
    occasion INTEGER NOT NULL,
    trait_extraversion REAL,
    trait_conscientiousness REAL,
    trait_neuroticism REAL,
    state_extraversion REAL,
    state_conscientiousness REAL,
    state_neuroticism REAL,
    situation_valence REAL,
    situation_sociality REAL,
    situation_demand REAL,
    situation_evaluation REAL,
    positive_affect REAL,
    negative_affect REAL,
    goal_pressure REAL,
    autonomy_support REAL,
    state_inertia_marker REAL,
    dynamic_signature_score REAL
);

.mode csv
.import --skip 1 data/synthetic_personality_dynamics_data.csv personality_dynamics

.headers on
.mode column

SELECT assessment_context,
       COUNT(DISTINCT person_id) AS n_persons,
       COUNT(*) AS n_observations,
       ROUND(AVG(state_extraversion),3) AS state_extraversion_mean,
       ROUND(AVG(state_conscientiousness),3) AS state_conscientiousness_mean,
       ROUND(AVG(state_neuroticism),3) AS state_neuroticism_mean,
       ROUND(AVG(situation_sociality),3) AS situation_sociality_mean,
       ROUND(AVG(situation_demand),3) AS situation_demand_mean,
       ROUND(AVG(situation_evaluation),3) AS situation_evaluation_mean,
       ROUND(AVG(dynamic_signature_score),3) AS dynamic_signature_mean
FROM personality_dynamics
GROUP BY assessment_context
ORDER BY dynamic_signature_mean DESC;

SELECT person_id,
       COUNT(*) AS n_obs,
       ROUND(AVG(state_extraversion),3) AS mean_state_extraversion,
       ROUND(AVG(state_conscientiousness),3) AS mean_state_conscientiousness,
       ROUND(AVG(state_neuroticism),3) AS mean_state_neuroticism,
       ROUND(AVG(dynamic_signature_score),3) AS mean_dynamic_signature
FROM personality_dynamics
GROUP BY person_id
ORDER BY mean_dynamic_signature DESC
LIMIT 25;
