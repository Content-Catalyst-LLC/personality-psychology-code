-- Personality Disorders and Dimensional Diagnosis
-- SQLite schema and example queries

DROP TABLE IF EXISTS dimensional_personality_disorders;

CREATE TABLE dimensional_personality_disorders (
    participant_id TEXT PRIMARY KEY,
    clinical_context TEXT NOT NULL,
    negative_affectivity REAL NOT NULL,
    detachment REAL NOT NULL,
    antagonism REAL NOT NULL,
    disinhibition REAL NOT NULL,
    psychoticism REAL NOT NULL,
    anankastia REAL NOT NULL,
    identity_impairment REAL NOT NULL,
    self_direction_impairment REAL NOT NULL,
    empathy_impairment REAL NOT NULL,
    intimacy_impairment REAL NOT NULL,
    self_functioning REAL NOT NULL,
    interpersonal_functioning REAL NOT NULL,
    functioning_impairment REAL NOT NULL,
    maladaptive_trait_burden REAL NOT NULL,
    severity_trait_interaction REAL NOT NULL,
    borderline_pattern_indicator REAL NOT NULL,
    pd_severity REAL NOT NULL,
    risk_level REAL NOT NULL,
    treatment_engagement REAL NOT NULL,
    perceived_support REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_disorders_dimensional_diagnosis.csv dimensional_personality_disorders

.headers on
.mode column

-- Clinical-context summaries
SELECT
    clinical_context,
    COUNT(*) AS n,
    ROUND(AVG(functioning_impairment), 3) AS functioning_impairment_mean,
    ROUND(AVG(maladaptive_trait_burden), 3) AS trait_burden_mean,
    ROUND(AVG(pd_severity), 3) AS pd_severity_mean,
    ROUND(AVG(risk_level), 3) AS risk_level_mean,
    ROUND(AVG(treatment_engagement), 3) AS treatment_engagement_mean
FROM dimensional_personality_disorders
GROUP BY clinical_context
ORDER BY pd_severity_mean DESC;

-- Severity-band summaries
SELECT
    CASE
        WHEN pd_severity < 2.5 THEN 'lower_severity'
        WHEN pd_severity >= 2.5 AND pd_severity < 4.5 THEN 'moderate_severity'
        ELSE 'higher_severity'
    END AS severity_band,
    COUNT(*) AS n,
    ROUND(AVG(functioning_impairment), 3) AS functioning_impairment_mean,
    ROUND(AVG(maladaptive_trait_burden), 3) AS trait_burden_mean,
    ROUND(AVG(borderline_pattern_indicator), 3) AS borderline_pattern_mean,
    ROUND(AVG(risk_level), 3) AS risk_level_mean
FROM dimensional_personality_disorders
GROUP BY severity_band
ORDER BY pd_severity_mean;

-- Dominant trait approximation
WITH trait_long AS (
    SELECT participant_id, 'negative_affectivity' AS domain, negative_affectivity AS score FROM dimensional_personality_disorders
    UNION ALL SELECT participant_id, 'detachment', detachment FROM dimensional_personality_disorders
    UNION ALL SELECT participant_id, 'antagonism', antagonism FROM dimensional_personality_disorders
    UNION ALL SELECT participant_id, 'disinhibition', disinhibition FROM dimensional_personality_disorders
    UNION ALL SELECT participant_id, 'psychoticism', psychoticism FROM dimensional_personality_disorders
    UNION ALL SELECT participant_id, 'anankastia', anankastia FROM dimensional_personality_disorders
),
dominant AS (
    SELECT participant_id, domain, score
    FROM trait_long t
    WHERE score = (
        SELECT MAX(score)
        FROM trait_long t2
        WHERE t2.participant_id = t.participant_id
    )
)
SELECT
    d.domain AS dominant_trait_domain,
    COUNT(*) AS n,
    ROUND(AVG(p.pd_severity), 3) AS pd_severity_mean,
    ROUND(AVG(p.functioning_impairment), 3) AS functioning_impairment_mean,
    ROUND(AVG(p.risk_level), 3) AS risk_level_mean
FROM dominant d
JOIN dimensional_personality_disorders p
  ON p.participant_id = d.participant_id
GROUP BY d.domain
ORDER BY pd_severity_mean DESC;
