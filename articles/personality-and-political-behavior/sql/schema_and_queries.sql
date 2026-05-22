-- Personality and Political Behavior
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_politics;

CREATE TABLE personality_politics (
    participant_id TEXT PRIMARY KEY,
    country_context TEXT NOT NULL,
    political_system_type TEXT NOT NULL,
    extraversion REAL NOT NULL,
    agreeableness REAL NOT NULL,
    conscientiousness REAL NOT NULL,
    neuroticism REAL NOT NULL,
    openness REAL NOT NULL,
    political_interest REAL NOT NULL,
    political_efficacy REAL NOT NULL,
    group_identity_strength REAL NOT NULL,
    perceived_threat REAL NOT NULL,
    media_exposure REAL NOT NULL,
    civic_opportunity REAL NOT NULL,
    ideology_score REAL NOT NULL,
    political_participation REAL NOT NULL,
    affective_polarization REAL NOT NULL,
    trust_in_institutions REAL NOT NULL,
    leadership_authority_preference REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_political_behavior.csv personality_politics

.headers on
.mode column

-- Context summaries
SELECT
    country_context,
    COUNT(*) AS n,
    ROUND(AVG(ideology_score), 3) AS ideology_mean,
    ROUND(AVG(political_participation), 3) AS participation_mean,
    ROUND(AVG(affective_polarization), 3) AS affective_polarization_mean,
    ROUND(AVG(trust_in_institutions), 3) AS institutional_trust_mean
FROM personality_politics
GROUP BY country_context
ORDER BY country_context;

-- Participation pathway summary
SELECT
    political_system_type,
    COUNT(*) AS n,
    ROUND(AVG(political_interest), 3) AS interest_mean,
    ROUND(AVG(political_efficacy), 3) AS efficacy_mean,
    ROUND(AVG(civic_opportunity), 3) AS opportunity_mean,
    ROUND(AVG(political_participation), 3) AS participation_mean
FROM personality_politics
GROUP BY political_system_type
ORDER BY participation_mean DESC;

-- Identity-threat polarization composite
SELECT
    country_context,
    ROUND(AVG((group_identity_strength + perceived_threat + media_exposure) / 3.0), 3) AS identity_threat_exposure,
    ROUND(AVG(affective_polarization), 3) AS affective_polarization_mean
FROM personality_politics
GROUP BY country_context
ORDER BY affective_polarization_mean DESC;
