DROP TABLE IF EXISTS maladaptive_personality;

CREATE TABLE maladaptive_personality (
    participant_id TEXT PRIMARY KEY,
    clinical_context TEXT NOT NULL,
    negative_affectivity REAL,
    detachment REAL,
    antagonism REAL,
    disinhibition REAL,
    psychoticism REAL,
    anankastia REAL,
    identity_impairment REAL,
    self_direction_impairment REAL,
    empathy_impairment REAL,
    intimacy_impairment REAL,
    self_functioning_impairment REAL,
    interpersonal_functioning_impairment REAL,
    functioning_impairment REAL,
    maladaptive_trait_burden REAL,
    severity_trait_interaction REAL,
    rigidity REAL,
    pervasiveness REAL,
    contextual_stress REAL,
    perceived_support REAL,
    clinical_severity REAL,
    clinical_liability REAL,
    threshold_zone_indicator REAL
);

.mode csv
.import --skip 1 data/synthetic_maladaptive_personality_structure.csv maladaptive_personality

.headers on
.mode column

SELECT clinical_context, COUNT(*) AS n,
       ROUND(AVG(functioning_impairment),3) AS functioning_mean,
       ROUND(AVG(maladaptive_trait_burden),3) AS trait_burden_mean,
       ROUND(AVG(clinical_severity),3) AS severity_mean,
       ROUND(AVG(clinical_liability),3) AS liability_mean
FROM maladaptive_personality
GROUP BY clinical_context
ORDER BY severity_mean DESC;

SELECT CASE
         WHEN clinical_severity < 2.5 THEN 'lower_severity'
         WHEN clinical_severity < 4.5 THEN 'moderate_severity'
         ELSE 'higher_severity'
       END AS severity_band,
       COUNT(*) AS n,
       ROUND(AVG(rigidity),3) AS rigidity_mean,
       ROUND(AVG(pervasiveness),3) AS pervasiveness_mean,
       ROUND(AVG(threshold_zone_indicator),3) AS threshold_zone_mean
FROM maladaptive_personality
GROUP BY severity_band;
