DROP TABLE IF EXISTS dark_traits_virtue;

CREATE TABLE dark_traits_virtue (
    participant_id TEXT PRIMARY KEY,
    institutional_context TEXT NOT NULL,
    machiavellianism REAL,
    narcissism REAL,
    psychopathy REAL,
    sadism REAL,
    honesty_humility REAL,
    conscientious_reliability REAL,
    fairness_orientation REAL,
    compassion_kindness REAL,
    moral_identity REAL,
    practical_judgment REAL,
    institutional_accountability REAL,
    status_reward_pressure REAL,
    unethical_behavior REAL,
    prosocial_restraint REAL,
    harm_indicator REAL,
    dark_trait_burden REAL,
    virtue_relevant_tendency REAL,
    moral_integration_index REAL,
    dark_accountability_risk REAL
);

.mode csv
.import --skip 1 data/synthetic_dark_traits_virtue_personality.csv dark_traits_virtue

.headers on
.mode column

SELECT institutional_context, COUNT(*) AS n,
       ROUND(AVG(dark_trait_burden),3) AS dark_mean,
       ROUND(AVG(virtue_relevant_tendency),3) AS virtue_mean,
       ROUND(AVG(institutional_accountability),3) AS accountability_mean,
       ROUND(AVG(unethical_behavior),3) AS unethical_mean,
       ROUND(AVG(harm_indicator),3) AS harm_mean
FROM dark_traits_virtue
GROUP BY institutional_context
ORDER BY harm_mean DESC;

SELECT CASE
         WHEN dark_trait_burden >= 4.0 AND virtue_relevant_tendency >= 4.0 THEN 'higher_dark_higher_virtue_relevant'
         WHEN dark_trait_burden >= 4.0 AND virtue_relevant_tendency < 4.0 THEN 'higher_dark_lower_virtue_relevant'
         WHEN dark_trait_burden < 4.0 AND virtue_relevant_tendency >= 4.0 THEN 'lower_dark_higher_virtue_relevant'
         ELSE 'lower_dark_lower_virtue_relevant'
       END AS moral_profile,
       COUNT(*) AS n,
       ROUND(AVG(unethical_behavior),3) AS unethical_mean,
       ROUND(AVG(prosocial_restraint),3) AS prosocial_mean,
       ROUND(AVG(harm_indicator),3) AS harm_mean
FROM dark_traits_virtue
GROUP BY moral_profile;
