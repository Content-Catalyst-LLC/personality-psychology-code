DROP TABLE IF EXISTS narrative_identity;

CREATE TABLE narrative_identity (
    person_id TEXT PRIMARY KEY,
    narrative_context TEXT NOT NULL,
    redemption REAL,
    contamination REAL,
    coherence REAL,
    agency REAL,
    communion REAL,
    meaning_making REAL,
    narrative_flexibility REAL,
    defensive_rigidity REAL,
    self_continuity REAL,
    well_being REAL,
    narrative_growth_orientation REAL,
    narrative_burden REAL,
    narrative_integration REAL,
    redemptive_agency_balance REAL
);

.mode csv
.import --skip 1 data/synthetic_narrative_identity.csv narrative_identity

.headers on
.mode column

SELECT narrative_context, COUNT(*) AS n,
       ROUND(AVG(redemption),3) AS redemption_mean,
       ROUND(AVG(contamination),3) AS contamination_mean,
       ROUND(AVG(coherence),3) AS coherence_mean,
       ROUND(AVG(agency),3) AS agency_mean,
       ROUND(AVG(meaning_making),3) AS meaning_mean,
       ROUND(AVG(self_continuity),3) AS continuity_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM narrative_identity
GROUP BY narrative_context
ORDER BY wellbeing_mean DESC;

SELECT CASE
         WHEN redemption >= 4.5 AND contamination < 4.0 AND coherence >= 4.5 THEN 'higher_redemption_lower_contamination_higher_coherence'
         WHEN redemption < 4.5 AND contamination >= 4.0 AND coherence < 4.5 THEN 'lower_redemption_higher_contamination_lower_coherence'
         WHEN coherence >= 4.5 AND defensive_rigidity >= 4.5 THEN 'high_coherence_high_defensiveness'
         ELSE 'mixed_narrative_profile'
       END AS narrative_profile,
       COUNT(*) AS n,
       ROUND(AVG(narrative_integration),3) AS integration_mean,
       ROUND(AVG(self_continuity),3) AS continuity_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM narrative_identity
GROUP BY narrative_profile
ORDER BY wellbeing_mean DESC;
