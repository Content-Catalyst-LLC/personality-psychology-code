-- Personality, Wellbeing, and Mental Health
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_wellbeing;

CREATE TABLE personality_wellbeing (
    participant_id TEXT PRIMARY KEY,
    age_band TEXT NOT NULL,
    life_context TEXT NOT NULL,
    extraversion REAL NOT NULL,
    agreeableness REAL NOT NULL,
    conscientiousness REAL NOT NULL,
    neuroticism REAL NOT NULL,
    openness REAL NOT NULL,
    coping_effectiveness REAL NOT NULL,
    perceived_support REAL NOT NULL,
    stress_burden REAL NOT NULL,
    positive_affect REAL NOT NULL,
    negative_affect REAL NOT NULL,
    life_satisfaction REAL NOT NULL,
    meaning_purpose REAL NOT NULL,
    wellbeing_score REAL NOT NULL,
    distress_score REAL NOT NULL,
    flourishing_score REAL NOT NULL,
    social_functioning REAL NOT NULL,
    treatment_access REAL NOT NULL,
    sleep_quality REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_wellbeing_mental_health.csv personality_wellbeing

.headers on
.mode column

-- Life-context summaries
SELECT
    life_context,
    COUNT(*) AS n,
    ROUND(AVG(wellbeing_score), 3) AS wellbeing_mean,
    ROUND(AVG(distress_score), 3) AS distress_mean,
    ROUND(AVG(flourishing_score), 3) AS flourishing_mean,
    ROUND(AVG(perceived_support), 3) AS support_mean,
    ROUND(AVG(stress_burden), 3) AS stress_burden_mean
FROM personality_wellbeing
GROUP BY life_context
ORDER BY wellbeing_mean DESC;

-- Age-band summaries
SELECT
    age_band,
    COUNT(*) AS n,
    ROUND(AVG(positive_affect), 3) AS positive_affect_mean,
    ROUND(AVG(negative_affect), 3) AS negative_affect_mean,
    ROUND(AVG(life_satisfaction), 3) AS life_satisfaction_mean,
    ROUND(AVG(meaning_purpose), 3) AS meaning_purpose_mean
FROM personality_wellbeing
GROUP BY age_band
ORDER BY age_band;

-- Two-continua profile approximation
SELECT
    CASE
        WHEN distress_score >= 4.5 AND flourishing_score >= 4.5 THEN 'higher_distress_higher_flourishing'
        WHEN distress_score >= 4.5 AND flourishing_score < 4.5 THEN 'higher_distress_lower_flourishing'
        WHEN distress_score < 4.5 AND flourishing_score >= 4.5 THEN 'lower_distress_higher_flourishing'
        ELSE 'lower_distress_lower_flourishing'
    END AS mental_health_profile,
    COUNT(*) AS n,
    ROUND(AVG(neuroticism), 3) AS neuroticism_mean,
    ROUND(AVG(extraversion), 3) AS extraversion_mean,
    ROUND(AVG(conscientiousness), 3) AS conscientiousness_mean,
    ROUND(AVG(perceived_support), 3) AS support_mean
FROM personality_wellbeing
GROUP BY mental_health_profile
ORDER BY mental_health_profile;
