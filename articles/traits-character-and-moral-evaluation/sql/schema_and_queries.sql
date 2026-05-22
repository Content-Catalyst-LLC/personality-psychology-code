DROP TABLE IF EXISTS traits_character;

CREATE TABLE traits_character (
    participant_id TEXT PRIMARY KEY,
    evaluation_context TEXT NOT NULL,
    honesty_humility REAL,
    conscientiousness REAL,
    agreeableness REAL,
    emotional_stability REAL,
    openness REAL,
    moral_identity REAL,
    practical_judgment REAL,
    institutional_accountability REAL,
    power_pressure REAL,
    social_desirability_pressure REAL,
    ethical_behavior REAL,
    integrity_rating REAL,
    trustworthiness_rating REAL,
    descriptive_trait_reliability REAL,
    moral_character_index REAL,
    judgment_context_index REAL,
    trait_character_gap REAL
);

.mode csv
.import --skip 1 data/synthetic_traits_character_morality.csv traits_character

.headers on
.mode column

SELECT evaluation_context, COUNT(*) AS n,
       ROUND(AVG(descriptive_trait_reliability),3) AS trait_reliability_mean,
       ROUND(AVG(moral_character_index),3) AS character_mean,
       ROUND(AVG(moral_identity),3) AS moral_identity_mean,
       ROUND(AVG(practical_judgment),3) AS practical_judgment_mean,
       ROUND(AVG(institutional_accountability),3) AS accountability_mean
FROM traits_character
GROUP BY evaluation_context
ORDER BY character_mean DESC;

SELECT CASE
         WHEN descriptive_trait_reliability >= 4.0 AND moral_character_index >= 4.0 THEN 'higher_trait_higher_character'
         WHEN descriptive_trait_reliability >= 4.0 AND moral_character_index < 4.0 THEN 'higher_trait_lower_character'
         WHEN descriptive_trait_reliability < 4.0 AND moral_character_index >= 4.0 THEN 'lower_trait_higher_character'
         ELSE 'lower_trait_lower_character'
       END AS trait_character_profile,
       COUNT(*) AS n,
       ROUND(AVG(ethical_behavior),3) AS ethical_behavior_mean,
       ROUND(AVG(integrity_rating),3) AS integrity_mean,
       ROUND(AVG(trustworthiness_rating),3) AS trustworthiness_mean
FROM traits_character
GROUP BY trait_character_profile;
