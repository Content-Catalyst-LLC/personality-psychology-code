DROP TABLE IF EXISTS personality_change;

CREATE TABLE personality_change (
    person_id TEXT NOT NULL,
    wave TEXT NOT NULL,
    wave_numeric INTEGER NOT NULL,
    intervention_group TEXT NOT NULL,
    age REAL,
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
.import --skip 1 data/synthetic_personality_change_intervention.csv personality_change

.headers on
.mode column

SELECT wave, intervention_group, COUNT(*) AS n,
       ROUND(AVG(neuroticism),3) AS neuroticism_mean,
       ROUND(AVG(extraversion),3) AS extraversion_mean,
       ROUND(AVG(conscientiousness),3) AS conscientiousness_mean,
       ROUND(AVG(openness),3) AS openness_mean,
       ROUND(AVG(agreeableness),3) AS agreeableness_mean,
       ROUND(AVG(role_investment),3) AS role_investment_mean,
       ROUND(AVG(state_practice_frequency),3) AS state_practice_mean,
       ROUND(AVG(perceived_support),3) AS support_mean
FROM personality_change
GROUP BY wave, intervention_group
ORDER BY wave_numeric, intervention_group;

WITH first_last AS (
  SELECT
    p.person_id,
    p.intervention_group,
    MAX(CASE WHEN p.wave_numeric = 1 THEN p.neuroticism END) AS neuroticism_first,
    MAX(CASE WHEN p.wave_numeric = 4 THEN p.neuroticism END) AS neuroticism_last,
    MAX(CASE WHEN p.wave_numeric = 1 THEN p.extraversion END) AS extraversion_first,
    MAX(CASE WHEN p.wave_numeric = 4 THEN p.extraversion END) AS extraversion_last,
    MAX(CASE WHEN p.wave_numeric = 1 THEN p.conscientiousness END) AS conscientiousness_first,
    MAX(CASE WHEN p.wave_numeric = 4 THEN p.conscientiousness END) AS conscientiousness_last
  FROM personality_change p
  GROUP BY p.person_id, p.intervention_group
)
SELECT intervention_group,
       COUNT(*) AS n,
       ROUND(AVG(neuroticism_last - neuroticism_first),3) AS neuroticism_change,
       ROUND(AVG(extraversion_last - extraversion_first),3) AS extraversion_change,
       ROUND(AVG(conscientiousness_last - conscientiousness_first),3) AS conscientiousness_change
FROM first_last
GROUP BY intervention_group;
