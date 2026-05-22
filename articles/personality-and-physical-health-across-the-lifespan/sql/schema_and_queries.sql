-- Personality and Physical Health Across the Lifespan
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_health;

CREATE TABLE personality_health (
    person_id TEXT NOT NULL,
    wave INTEGER NOT NULL,
    age REAL NOT NULL,
    age_band TEXT NOT NULL,
    life_context TEXT NOT NULL,
    extraversion REAL NOT NULL,
    agreeableness REAL NOT NULL,
    conscientiousness REAL NOT NULL,
    neuroticism REAL NOT NULL,
    openness REAL NOT NULL,
    emotional_stability REAL NOT NULL,
    perceived_support REAL NOT NULL,
    exercise REAL NOT NULL,
    sleep_quality REAL NOT NULL,
    smoking_risk REAL NOT NULL,
    alcohol_risk REAL NOT NULL,
    medication_adherence REAL NOT NULL,
    stress_burden REAL NOT NULL,
    physical_health_score REAL NOT NULL,
    functional_ability REAL NOT NULL,
    chronic_condition_burden REAL NOT NULL,
    PRIMARY KEY (person_id, wave)
);

.mode csv
.import --skip 1 data/synthetic_personality_physical_health_lifespan.csv personality_health

.headers on
.mode column

-- Age-band summaries
SELECT
    age_band,
    COUNT(*) AS observations,
    ROUND(AVG(physical_health_score), 3) AS physical_health_mean,
    ROUND(AVG(functional_ability), 3) AS functional_ability_mean,
    ROUND(AVG(chronic_condition_burden), 3) AS chronic_condition_burden_mean,
    ROUND(AVG(stress_burden), 3) AS stress_burden_mean
FROM personality_health
GROUP BY age_band
ORDER BY MIN(age);

-- Life-context summaries
SELECT
    life_context,
    COUNT(*) AS observations,
    ROUND(AVG(perceived_support), 3) AS perceived_support_mean,
    ROUND(AVG(medication_adherence), 3) AS medication_adherence_mean,
    ROUND(AVG(physical_health_score), 3) AS physical_health_mean,
    ROUND(AVG(functional_ability), 3) AS functional_ability_mean
FROM personality_health
GROUP BY life_context
ORDER BY physical_health_mean DESC;

-- Health behavior and stress vulnerability indicators
SELECT
    age_band,
    ROUND(AVG((exercise + sleep_quality + medication_adherence - smoking_risk - alcohol_risk) / 3.0), 3) AS health_behavior_index,
    ROUND(AVG(neuroticism + stress_burden - emotional_stability - perceived_support), 3) AS stress_vulnerability_index
FROM personality_health
GROUP BY age_band
ORDER BY MIN(age);
