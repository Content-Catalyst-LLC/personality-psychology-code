DROP TABLE IF EXISTS personality_lifespan;

CREATE TABLE personality_lifespan (
    person_id TEXT NOT NULL,
    wave TEXT NOT NULL,
    wave_numeric INTEGER NOT NULL,
    age REAL,
    life_stage TEXT,
    cohort TEXT,
    cultural_context TEXT,
    neuroticism REAL,
    extraversion REAL,
    conscientiousness REAL,
    openness REAL,
    agreeableness REAL,
    role_investment REAL,
    state_practice_frequency REAL,
    perceived_support REAL,
    PRIMARY KEY (person_id, wave_numeric)
);

.mode csv
.import --skip 1 data/synthetic_personality_lifespan.csv personality_lifespan

.headers on
.mode column

SELECT life_stage, COUNT(*) AS n,
       ROUND(AVG(age),3) AS age_mean,
       ROUND(AVG(neuroticism),3) AS neuroticism_mean,
       ROUND(AVG(extraversion),3) AS extraversion_mean,
       ROUND(AVG(conscientiousness),3) AS conscientiousness_mean,
       ROUND(AVG(openness),3) AS openness_mean,
       ROUND(AVG(agreeableness),3) AS agreeableness_mean,
       ROUND(AVG(role_investment),3) AS role_investment_mean,
       ROUND(AVG(perceived_support),3) AS support_mean
FROM personality_lifespan
GROUP BY life_stage
ORDER BY age_mean;

SELECT wave, COUNT(*) AS n,
       ROUND(AVG(neuroticism),3) AS neuroticism_mean,
       ROUND(AVG(extraversion),3) AS extraversion_mean,
       ROUND(AVG(conscientiousness),3) AS conscientiousness_mean,
       ROUND(AVG(openness),3) AS openness_mean,
       ROUND(AVG(agreeableness),3) AS agreeableness_mean
FROM personality_lifespan
GROUP BY wave, wave_numeric
ORDER BY wave_numeric;

WITH first_last AS (
  SELECT
    p.person_id,
    p.cohort,
    p.cultural_context,
    MAX(CASE WHEN p.wave_numeric = 1 THEN p.neuroticism END) AS neuroticism_first,
    MAX(CASE WHEN p.wave_numeric = 6 THEN p.neuroticism END) AS neuroticism_last,
    MAX(CASE WHEN p.wave_numeric = 1 THEN p.conscientiousness END) AS conscientiousness_first,
    MAX(CASE WHEN p.wave_numeric = 6 THEN p.conscientiousness END) AS conscientiousness_last,
    MAX(CASE WHEN p.wave_numeric = 1 THEN p.openness END) AS openness_first,
    MAX(CASE WHEN p.wave_numeric = 6 THEN p.openness END) AS openness_last
  FROM personality_lifespan p
  GROUP BY p.person_id, p.cohort, p.cultural_context
)
SELECT cohort, cultural_context, COUNT(*) AS n,
       ROUND(AVG(neuroticism_last - neuroticism_first),3) AS neuroticism_change,
       ROUND(AVG(conscientiousness_last - conscientiousness_first),3) AS conscientiousness_change,
       ROUND(AVG(openness_last - openness_first),3) AS openness_change
FROM first_last
GROUP BY cohort, cultural_context
ORDER BY cohort, cultural_context;
