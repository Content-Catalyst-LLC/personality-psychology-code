-- SQLite schema and analytic queries for synthetic personality-creativity data.

DROP TABLE IF EXISTS personality_creativity;

CREATE TABLE personality_creativity (
  id INTEGER PRIMARY KEY,
  openness REAL,
  intellect REAL,
  conscientiousness REAL,
  extraversion REAL,
  agreeableness REAL,
  neuroticism REAL,
  persistence REAL,
  social_support REAL,
  domain TEXT,
  divergent_thinking REAL,
  creative_achievement REAL,
  everyday_creativity REAL
);

.mode csv
.import --skip 1 data/synthetic_personality_creativity.csv personality_creativity

.headers on
.mode column

.output outputs/tables/sql_domain_summary.txt
SELECT
  domain,
  COUNT(*) AS n,
  ROUND(AVG(openness), 2) AS mean_openness,
  ROUND(AVG(intellect), 2) AS mean_intellect,
  ROUND(AVG(divergent_thinking), 2) AS mean_divergent_thinking,
  ROUND(AVG(creative_achievement), 2) AS mean_creative_achievement,
  ROUND(AVG(everyday_creativity), 2) AS mean_everyday_creativity
FROM personality_creativity
GROUP BY domain
ORDER BY domain;

.output outputs/tables/sql_high_support_cases.txt
SELECT
  id,
  domain,
  openness,
  intellect,
  persistence,
  social_support,
  creative_achievement
FROM personality_creativity
WHERE social_support >= 75
ORDER BY creative_achievement DESC;

.output stdout
SELECT 'SQL analysis complete. Outputs written to outputs/tables/.' AS status;
