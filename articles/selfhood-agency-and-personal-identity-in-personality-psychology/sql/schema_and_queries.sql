DROP TABLE IF EXISTS selfhood_agency_identity;

CREATE TABLE selfhood_agency_identity (
    person_id TEXT PRIMARY KEY,
    identity_context TEXT NOT NULL,
    past_self REAL,
    present_self REAL,
    future_self REAL,
    intentional_clarity REAL,
    action_ownership REAL,
    self_efficacy REAL,
    external_constraint REAL,
    social_recognition REAL,
    value_commitment_gap REAL,
    identity_integration REAL,
    well_being REAL,
    past_present_gap REAL,
    present_future_gap REAL,
    temporal_self_continuity REAL,
    agency_index REAL,
    situated_agency_index REAL,
    identity_alignment REAL
);

.mode csv
.import --skip 1 data/synthetic_selfhood_agency_identity.csv selfhood_agency_identity

.headers on
.mode column

SELECT identity_context, COUNT(*) AS n,
       ROUND(AVG(temporal_self_continuity),3) AS continuity_mean,
       ROUND(AVG(situated_agency_index),3) AS situated_agency_mean,
       ROUND(AVG(social_recognition),3) AS recognition_mean,
       ROUND(AVG(external_constraint),3) AS constraint_mean,
       ROUND(AVG(identity_integration),3) AS integration_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM selfhood_agency_identity
GROUP BY identity_context
ORDER BY integration_mean DESC;

SELECT CASE
         WHEN temporal_self_continuity >= 0.70 AND situated_agency_index >= 3.50 THEN 'higher_continuity_higher_agency'
         WHEN temporal_self_continuity >= 0.70 AND situated_agency_index < 3.50 THEN 'higher_continuity_lower_agency'
         WHEN temporal_self_continuity < 0.70 AND situated_agency_index >= 3.50 THEN 'lower_continuity_higher_agency'
         ELSE 'lower_continuity_lower_agency'
       END AS identity_profile,
       COUNT(*) AS n,
       ROUND(AVG(identity_integration),3) AS integration_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean,
       ROUND(AVG(external_constraint),3) AS constraint_mean,
       ROUND(AVG(social_recognition),3) AS recognition_mean
FROM selfhood_agency_identity
GROUP BY identity_profile
ORDER BY integration_mean DESC;
