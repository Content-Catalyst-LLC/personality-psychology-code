DROP TABLE IF EXISTS personality_measurement_psychometrics;

CREATE TABLE personality_measurement_psychometrics (
    person_id TEXT PRIMARY KEY,
    assessment_context TEXT NOT NULL,
    s1 REAL,
    s2 REAL,
    s3 REAL,
    s4 REAL,
    s5 REAL,
    o1 REAL,
    o2 REAL,
    o3 REAL,
    o4 REAL,
    o5 REAL,
    attention_check INTEGER,
    careless_response_risk REAL,
    social_desirability_pressure REAL,
    self_missing_count INTEGER,
    observer_missing_count INTEGER,
    self_conscientiousness REAL,
    observer_conscientiousness REAL,
    self_other_discrepancy REAL,
    absolute_self_other_discrepancy REAL,
    method_effect_index REAL,
    reliability_context_score REAL,
    professional_reflection_score REAL
);

.mode csv
.import --skip 1 data/synthetic_personality_measurement_data.csv personality_measurement_psychometrics

.headers on
.mode column

SELECT assessment_context,
       COUNT(*) AS n,
       ROUND(AVG(attention_check),3) AS attention_pass_rate,
       ROUND(AVG(careless_response_risk),3) AS careless_risk_mean,
       ROUND(AVG(social_desirability_pressure),3) AS social_desirability_mean,
       ROUND(AVG(self_conscientiousness),3) AS self_score_mean,
       ROUND(AVG(observer_conscientiousness),3) AS observer_score_mean,
       ROUND(AVG(absolute_self_other_discrepancy),3) AS absolute_discrepancy_mean,
       ROUND(AVG(method_effect_index),3) AS method_effect_mean,
       ROUND(AVG(reliability_context_score),3) AS reliability_context_mean
FROM personality_measurement_psychometrics
GROUP BY assessment_context
ORDER BY reliability_context_mean DESC;

SELECT person_id, assessment_context,
       self_conscientiousness,
       observer_conscientiousness,
       absolute_self_other_discrepancy,
       careless_response_risk,
       social_desirability_pressure,
       method_effect_index
FROM personality_measurement_psychometrics
ORDER BY absolute_self_other_discrepancy DESC
LIMIT 25;
