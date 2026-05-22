DROP TABLE IF EXISTS self_system;

CREATE TABLE self_system (
    person_id TEXT PRIMARY KEY,
    self_system_context TEXT NOT NULL,
    self_warmth REAL,
    self_conscientiousness REAL,
    self_emotional_stability REAL,
    self_openness REAL,
    other_warmth REAL,
    other_conscientiousness REAL,
    other_emotional_stability REAL,
    other_openness REAL,
    actual_self REAL,
    ideal_self REAL,
    ought_self REAL,
    self_esteem REAL,
    social_recognition REAL,
    external_devaluation REAL,
    well_being REAL,
    warmth_gap REAL,
    conscientiousness_gap REAL,
    emotional_stability_gap REAL,
    openness_gap REAL,
    self_other_gap_mean REAL,
    self_knowledge_accuracy REAL,
    actual_ideal_discrepancy REAL,
    actual_ought_discrepancy REAL,
    total_self_discrepancy REAL,
    self_concept_positivity REAL
);

.mode csv
.import --skip 1 data/synthetic_self_concept_self_esteem_self_knowledge.csv self_system

.headers on
.mode column

SELECT self_system_context, COUNT(*) AS n,
       ROUND(AVG(self_concept_positivity),3) AS self_concept_positivity_mean,
       ROUND(AVG(self_esteem),3) AS self_esteem_mean,
       ROUND(AVG(self_knowledge_accuracy),3) AS self_knowledge_accuracy_mean,
       ROUND(AVG(total_self_discrepancy),3) AS discrepancy_mean,
       ROUND(AVG(social_recognition),3) AS recognition_mean,
       ROUND(AVG(external_devaluation),3) AS devaluation_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM self_system
GROUP BY self_system_context
ORDER BY wellbeing_mean DESC;

SELECT CASE
         WHEN self_esteem >= 4.5 AND self_knowledge_accuracy < 0.70 THEN 'high_esteem_low_accuracy'
         WHEN self_esteem < 4.0 AND external_devaluation >= 4.5 THEN 'low_esteem_high_devaluation'
         WHEN total_self_discrepancy >= 2.0 THEN 'high_discrepancy'
         ELSE 'mixed_self_system_profile'
       END AS self_system_pattern,
       COUNT(*) AS n,
       ROUND(AVG(self_esteem),3) AS self_esteem_mean,
       ROUND(AVG(self_knowledge_accuracy),3) AS self_knowledge_accuracy_mean,
       ROUND(AVG(total_self_discrepancy),3) AS discrepancy_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM self_system
GROUP BY self_system_pattern
ORDER BY wellbeing_mean DESC;
