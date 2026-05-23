DROP TABLE IF EXISTS temperament_personality;

CREATE TABLE temperament_personality (
    child_id TEXT PRIMARY KEY,
    developmental_context TEXT NOT NULL,
    inhibition_t1 REAL,
    negative_affect_t1 REAL,
    surgency_t1 REAL,
    effortful_control_t1 REAL,
    parenting_support_t1 REAL,
    family_stress_t1 REAL,
    classroom_support_t2 REAL,
    peer_support_t2 REAL,
    institutional_stability_t2 REAL,
    conscientiousness_t2 REAL,
    neuroticism_t2 REAL,
    social_confidence_t2 REAL,
    regulation_skill_t2 REAL,
    reactivity_regulation_balance REAL,
    environmental_support_index REAL,
    developmental_risk_index REAL,
    adaptive_pathway_score REAL
);

.mode csv
.import --skip 1 data/synthetic_temperament_personality_longitudinal.csv temperament_personality

.headers on
.mode column

SELECT developmental_context,
       COUNT(*) AS n,
       ROUND(AVG(inhibition_t1),3) AS inhibition_mean,
       ROUND(AVG(negative_affect_t1),3) AS negative_affect_mean,
       ROUND(AVG(effortful_control_t1),3) AS effortful_control_mean,
       ROUND(AVG(parenting_support_t1),3) AS parenting_support_mean,
       ROUND(AVG(family_stress_t1),3) AS family_stress_mean,
       ROUND(AVG(conscientiousness_t2),3) AS conscientiousness_mean,
       ROUND(AVG(neuroticism_t2),3) AS neuroticism_mean,
       ROUND(AVG(social_confidence_t2),3) AS social_confidence_mean,
       ROUND(AVG(regulation_skill_t2),3) AS regulation_skill_mean,
       ROUND(AVG(developmental_risk_index),3) AS risk_mean,
       ROUND(AVG(adaptive_pathway_score),3) AS adaptive_pathway_mean
FROM temperament_personality
GROUP BY developmental_context
ORDER BY adaptive_pathway_mean DESC;
