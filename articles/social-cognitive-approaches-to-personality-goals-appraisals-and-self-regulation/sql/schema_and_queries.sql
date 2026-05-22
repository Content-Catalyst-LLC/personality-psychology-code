DROP TABLE IF EXISTS social_cognitive_personality;

CREATE TABLE social_cognitive_personality (
    person_id TEXT NOT NULL,
    occasion INTEGER NOT NULL,
    situation_type TEXT NOT NULL,
    goal_activation REAL,
    threat_appraisal REAL,
    challenge_appraisal REAL,
    self_efficacy REAL,
    self_regulation REAL,
    emotional_arousal REAL,
    perceived_support REAL,
    prosocial_behavior REAL,
    avoidance_behavior REAL,
    task_persistence REAL,
    appraisal_balance REAL,
    regulation_capacity REAL,
    approach_orientation REAL,
    avoidance_pressure REAL,
    PRIMARY KEY (person_id, occasion)
);

.mode csv
.import --skip 1 data/synthetic_social_cognitive_personality.csv social_cognitive_personality

.headers on
.mode column

SELECT situation_type, COUNT(*) AS n,
       ROUND(AVG(goal_activation),3) AS goal_mean,
       ROUND(AVG(threat_appraisal),3) AS threat_mean,
       ROUND(AVG(challenge_appraisal),3) AS challenge_mean,
       ROUND(AVG(self_efficacy),3) AS efficacy_mean,
       ROUND(AVG(self_regulation),3) AS regulation_mean,
       ROUND(AVG(prosocial_behavior),3) AS prosocial_mean,
       ROUND(AVG(avoidance_behavior),3) AS avoidance_mean,
       ROUND(AVG(task_persistence),3) AS persistence_mean
FROM social_cognitive_personality
GROUP BY situation_type
ORDER BY persistence_mean DESC;

SELECT person_id,
       COUNT(*) AS n_occasions,
       ROUND(AVG(appraisal_balance),3) AS appraisal_balance_mean,
       ROUND(AVG(regulation_capacity),3) AS regulation_capacity_mean,
       ROUND(AVG(prosocial_behavior),3) AS prosocial_mean,
       ROUND(AVG(avoidance_behavior),3) AS avoidance_mean,
       ROUND(AVG(task_persistence),3) AS persistence_mean
FROM social_cognitive_personality
GROUP BY person_id
ORDER BY persistence_mean DESC
LIMIT 20;
