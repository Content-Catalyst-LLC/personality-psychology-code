-- Personality and Institutions: Leadership, Bureaucracy, and Social Order
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_institutions;

CREATE TABLE personality_institutions (
    participant_id TEXT PRIMARY KEY,
    institutional_unit TEXT NOT NULL,
    role_type TEXT NOT NULL,
    conscientiousness REAL NOT NULL,
    agreeableness REAL NOT NULL,
    emotional_stability REAL NOT NULL,
    openness REAL NOT NULL,
    dark_trait_pressure REAL NOT NULL,
    bureaucratic_fit REAL NOT NULL,
    discretion_level REAL NOT NULL,
    accountability_strength REAL NOT NULL,
    leadership_rating REAL NOT NULL,
    institutional_performance REAL NOT NULL,
    institutional_trust REAL NOT NULL,
    role_clarity REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_institutions_bureaucracy.csv personality_institutions

.headers on
.mode column

-- Institutional-unit summaries
SELECT
    institutional_unit,
    COUNT(*) AS n,
    ROUND(AVG(bureaucratic_fit), 3) AS bureaucratic_fit_mean,
    ROUND(AVG(discretion_level), 3) AS discretion_mean,
    ROUND(AVG(accountability_strength), 3) AS accountability_mean,
    ROUND(AVG(institutional_performance), 3) AS performance_mean,
    ROUND(AVG(institutional_trust), 3) AS trust_mean
FROM personality_institutions
GROUP BY institutional_unit
ORDER BY institutional_unit;

-- Role-type summaries
SELECT
    role_type,
    COUNT(*) AS n,
    ROUND(AVG(leadership_rating), 3) AS leadership_mean,
    ROUND(AVG(institutional_performance), 3) AS performance_mean,
    ROUND(AVG(institutional_trust), 3) AS trust_mean,
    ROUND(AVG(discretion_level - accountability_strength - bureaucratic_fit), 3) AS institutional_risk_index
FROM personality_institutions
GROUP BY role_type
ORDER BY institutional_risk_index DESC;

-- Stewardship-oriented composite
SELECT
    institutional_unit,
    ROUND(AVG((conscientiousness + agreeableness + emotional_stability + bureaucratic_fit + accountability_strength) / 5.0), 3) AS stewardship_composite,
    ROUND(AVG(institutional_trust), 3) AS trust_mean
FROM personality_institutions
GROUP BY institutional_unit
ORDER BY stewardship_composite DESC;
