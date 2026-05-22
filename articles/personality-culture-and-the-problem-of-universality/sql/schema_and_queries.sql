-- Personality, Culture, and the Problem of Universality
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_culture;

CREATE TABLE personality_culture (
    participant_id TEXT PRIMARY KEY,
    culture_group TEXT NOT NULL,
    openness REAL NOT NULL,
    conscientiousness REAL NOT NULL,
    extraversion REAL NOT NULL,
    agreeableness REAL NOT NULL,
    neuroticism REAL NOT NULL,
    honesty_humility REAL NOT NULL,
    context_collectivism REAL NOT NULL,
    behavioral_manifestation REAL NOT NULL,
    survey_language_family TEXT NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_culture_universality.csv personality_culture

.headers on
.mode column

-- Group summaries
SELECT
    culture_group,
    COUNT(*) AS n,
    ROUND(AVG(openness), 3) AS openness_mean,
    ROUND(AVG(conscientiousness), 3) AS conscientiousness_mean,
    ROUND(AVG(extraversion), 3) AS extraversion_mean,
    ROUND(AVG(agreeableness), 3) AS agreeableness_mean,
    ROUND(AVG(neuroticism), 3) AS neuroticism_mean,
    ROUND(AVG(honesty_humility), 3) AS honesty_humility_mean,
    ROUND(AVG(context_collectivism), 3) AS context_collectivism_mean,
    ROUND(AVG(behavioral_manifestation), 3) AS behavioral_manifestation_mean
FROM personality_culture
GROUP BY culture_group
ORDER BY culture_group;

-- Trait-context behavioral manifestation example
SELECT
    culture_group,
    ROUND(AVG((conscientiousness + agreeableness + honesty_humility) / 3.0), 3) AS prosocial_trait_composite,
    ROUND(AVG(context_collectivism), 3) AS context_collectivism,
    ROUND(AVG(behavioral_manifestation), 3) AS behavioral_manifestation
FROM personality_culture
GROUP BY culture_group
ORDER BY behavioral_manifestation DESC;
