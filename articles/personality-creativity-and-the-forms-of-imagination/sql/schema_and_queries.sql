-- SQLite workflow for synthetic personality-creativity data.
-- Run from article directory:
-- sqlite3 outputs/tables/personality_creativity.sqlite < sql/schema_and_queries.sql

DROP TABLE IF EXISTS personality_creativity;

CREATE TABLE personality_creativity (
  participant_id TEXT PRIMARY KEY,
  domain TEXT NOT NULL,
  openness REAL NOT NULL,
  intellect REAL NOT NULL,
  conscientiousness REAL NOT NULL,
  extraversion REAL NOT NULL,
  agreeableness REAL NOT NULL,
  neuroticism REAL NOT NULL,
  persistence REAL NOT NULL,
  social_support REAL NOT NULL,
  divergent_thinking REAL NOT NULL,
  creative_achievement REAL NOT NULL,
  everyday_creativity REAL NOT NULL
);

.mode csv
.import --skip 1 data/synthetic_personality_creativity.csv personality_creativity

.headers on
.mode column

-- Domain-level outcome summaries.
SELECT
  domain,
  ROUND(AVG(openness), 2) AS mean_openness,
  ROUND(AVG(intellect), 2) AS mean_intellect,
  ROUND(AVG(persistence), 2) AS mean_persistence,
  ROUND(AVG(divergent_thinking), 2) AS mean_divergent_thinking,
  ROUND(AVG(creative_achievement), 2) AS mean_creative_achievement,
  ROUND(AVG(everyday_creativity), 2) AS mean_everyday_creativity
FROM personality_creativity
GROUP BY domain
ORDER BY domain;

-- High-level synthetic profile records.
SELECT
  participant_id,
  domain,
  openness,
  intellect,
  persistence,
  social_support,
  divergent_thinking,
  creative_achievement,
  everyday_creativity
FROM personality_creativity
ORDER BY creative_achievement DESC
LIMIT 10;
