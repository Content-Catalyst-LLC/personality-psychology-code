-- Personality, Work, and Leadership
-- SQLite schema and example queries

DROP TABLE IF EXISTS personality_work;

CREATE TABLE personality_work (
    participant_id TEXT PRIMARY KEY,
    role_family TEXT NOT NULL,
    organizational_context TEXT NOT NULL,
    extraversion REAL NOT NULL,
    agreeableness REAL NOT NULL,
    conscientiousness REAL NOT NULL,
    neuroticism REAL NOT NULL,
    openness REAL NOT NULL,
    emotional_stability REAL NOT NULL,
    dark_trait_pressure REAL NOT NULL,
    role_fit REAL NOT NULL,
    accountability REAL NOT NULL,
    job_performance REAL NOT NULL,
    leadership_emergence REAL NOT NULL,
    leadership_effectiveness REAL NOT NULL,
    counterproductive_work_behavior REAL NOT NULL,
    teamwork_quality REAL NOT NULL,
    burnout_risk REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_work_leadership.csv personality_work

.headers on
.mode column

-- Role-family summaries
SELECT
    role_family,
    COUNT(*) AS n,
    ROUND(AVG(job_performance), 3) AS job_performance_mean,
    ROUND(AVG(leadership_emergence), 3) AS leadership_emergence_mean,
    ROUND(AVG(leadership_effectiveness), 3) AS leadership_effectiveness_mean,
    ROUND(AVG(teamwork_quality), 3) AS teamwork_mean,
    ROUND(AVG(counterproductive_work_behavior), 3) AS cwb_mean
FROM personality_work
GROUP BY role_family
ORDER BY role_family;

-- Organizational-context summaries
SELECT
    organizational_context,
    COUNT(*) AS n,
    ROUND(AVG(role_fit), 3) AS role_fit_mean,
    ROUND(AVG(accountability), 3) AS accountability_mean,
    ROUND(AVG(job_performance), 3) AS performance_mean,
    ROUND(AVG(burnout_risk), 3) AS burnout_risk_mean
FROM personality_work
GROUP BY organizational_context
ORDER BY organizational_context;

-- Stewardship and derailment indicators
SELECT
    role_family,
    ROUND(AVG((conscientiousness + agreeableness + emotional_stability + accountability - dark_trait_pressure) / 4.0), 3) AS stewardship_index,
    ROUND(AVG(dark_trait_pressure + neuroticism - accountability - role_fit), 3) AS derailment_risk_index
FROM personality_work
GROUP BY role_family
ORDER BY derailment_risk_index DESC;
