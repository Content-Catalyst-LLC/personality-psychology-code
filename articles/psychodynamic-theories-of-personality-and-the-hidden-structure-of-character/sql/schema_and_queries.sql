DROP TABLE IF EXISTS psychodynamic_personality;

CREATE TABLE psychodynamic_personality (
    person_id TEXT PRIMARY KEY,
    developmental_context TEXT NOT NULL,
    mature_defenses REAL,
    neurotic_defenses REAL,
    immature_defenses REAL,
    defensive_rigidity REAL,
    attachment_anxiety REAL,
    attachment_avoidance REAL,
    self_cohesion REAL,
    relational_security REAL,
    reflective_functioning REAL,
    character_integration REAL,
    symptom_distress REAL,
    defensive_maturity REAL,
    attachment_insecurity REAL,
    self_relational_capacity REAL,
    hidden_structure_risk REAL
);

.mode csv
.import --skip 1 data/synthetic_psychodynamic_personality.csv psychodynamic_personality

.headers on
.mode column

SELECT developmental_context, COUNT(*) AS n,
       ROUND(AVG(defensive_maturity),3) AS defensive_maturity_mean,
       ROUND(AVG(attachment_insecurity),3) AS attachment_insecurity_mean,
       ROUND(AVG(self_relational_capacity),3) AS self_relational_capacity_mean,
       ROUND(AVG(character_integration),3) AS character_integration_mean,
       ROUND(AVG(symptom_distress),3) AS symptom_distress_mean
FROM psychodynamic_personality
GROUP BY developmental_context
ORDER BY character_integration_mean DESC;

SELECT CASE
         WHEN mature_defenses > immature_defenses AND mature_defenses > neurotic_defenses THEN 'mature_defense_dominant'
         WHEN immature_defenses > mature_defenses AND immature_defenses > neurotic_defenses THEN 'immature_defense_dominant'
         WHEN neurotic_defenses > mature_defenses AND neurotic_defenses > immature_defenses THEN 'neurotic_defense_dominant'
         ELSE 'mixed_defensive_profile'
       END AS defense_profile,
       COUNT(*) AS n,
       ROUND(AVG(defensive_maturity),3) AS defensive_maturity_mean,
       ROUND(AVG(character_integration),3) AS character_integration_mean,
       ROUND(AVG(symptom_distress),3) AS symptom_distress_mean
FROM psychodynamic_personality
GROUP BY defense_profile
ORDER BY symptom_distress_mean DESC;
