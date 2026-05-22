-- Personality, Relationships, and Social Functioning
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_relationships;

CREATE TABLE personality_relationships (
    participant_id TEXT PRIMARY KEY,
    social_context TEXT NOT NULL,
    relationship_domain TEXT NOT NULL,
    extraversion REAL NOT NULL,
    agreeableness REAL NOT NULL,
    conscientiousness REAL NOT NULL,
    neuroticism REAL NOT NULL,
    openness REAL NOT NULL,
    empathy REAL NOT NULL,
    self_regulation REAL NOT NULL,
    attachment_security REAL NOT NULL,
    perceived_support REAL NOT NULL,
    relationship_satisfaction REAL NOT NULL,
    social_functioning REAL NOT NULL,
    loneliness REAL NOT NULL,
    conflict_frequency REAL NOT NULL,
    reciprocity_quality REAL NOT NULL,
    reputation_trust REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_relationships_social_functioning.csv personality_relationships

.headers on
.mode column

-- Social-context summaries
SELECT
    social_context,
    COUNT(*) AS n,
    ROUND(AVG(relationship_satisfaction), 3) AS relationship_satisfaction_mean,
    ROUND(AVG(social_functioning), 3) AS social_functioning_mean,
    ROUND(AVG(loneliness), 3) AS loneliness_mean,
    ROUND(AVG(conflict_frequency), 3) AS conflict_frequency_mean,
    ROUND(AVG(perceived_support), 3) AS perceived_support_mean
FROM personality_relationships
GROUP BY social_context
ORDER BY social_context;

-- Relationship-domain summaries
SELECT
    relationship_domain,
    COUNT(*) AS n,
    ROUND(AVG(reciprocity_quality), 3) AS reciprocity_mean,
    ROUND(AVG(reputation_trust), 3) AS reputation_trust_mean,
    ROUND(AVG(relationship_satisfaction), 3) AS satisfaction_mean
FROM personality_relationships
GROUP BY relationship_domain
ORDER BY satisfaction_mean DESC;

-- Relational stability and conflict-risk indicators
SELECT
    relationship_domain,
    ROUND(AVG((agreeableness + conscientiousness + empathy + self_regulation + attachment_security - neuroticism) / 5.0), 3) AS relational_stability_index,
    ROUND(AVG(neuroticism + conflict_frequency - agreeableness - self_regulation), 3) AS conflict_risk_index
FROM personality_relationships
GROUP BY relationship_domain
ORDER BY conflict_risk_index DESC;
