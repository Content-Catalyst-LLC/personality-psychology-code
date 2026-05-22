DROP TABLE IF EXISTS motivation_goals_desire;

CREATE TABLE motivation_goals_desire (
    person_id TEXT PRIMARY KEY,
    motivation_context TEXT NOT NULL,
    autonomy_goal REAL,
    achievement_goal REAL,
    belonging_goal REAL,
    security_goal REAL,
    meaning_goal REAL,
    status_goal REAL,
    goal_conflict REAL,
    goal_ownership REAL,
    autonomy_support REAL,
    competence_support REAL,
    relatedness_support REAL,
    conscientiousness REAL,
    persistence_score REAL,
    adaptive_disengagement REAL,
    well_being REAL,
    total_goal_intensity REAL,
    approach_orientation REAL,
    avoidance_security_orientation REAL,
    status_orientation REAL,
    need_support REAL,
    motivational_quality REAL,
    life_direction_coherence REAL
);

.mode csv
.import --skip 1 data/synthetic_motivation_goals_desire.csv motivation_goals_desire

.headers on
.mode column

SELECT motivation_context, COUNT(*) AS n,
       ROUND(AVG(approach_orientation),3) AS approach_mean,
       ROUND(AVG(status_orientation),3) AS status_mean,
       ROUND(AVG(avoidance_security_orientation),3) AS security_mean,
       ROUND(AVG(need_support),3) AS need_support_mean,
       ROUND(AVG(goal_ownership),3) AS ownership_mean,
       ROUND(AVG(motivational_quality),3) AS quality_mean,
       ROUND(AVG(goal_conflict),3) AS conflict_mean,
       ROUND(AVG(persistence_score),3) AS persistence_mean,
       ROUND(AVG(adaptive_disengagement),3) AS disengagement_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM motivation_goals_desire
GROUP BY motivation_context
ORDER BY wellbeing_mean DESC;

SELECT CASE
         WHEN goal_conflict >= 4.5 AND goal_ownership < 4.0 THEN 'high_conflict_low_ownership'
         WHEN status_goal >= 4.5 AND meaning_goal < 4.0 THEN 'high_status_low_meaning'
         WHEN motivational_quality >= 4.5 AND goal_conflict < 4.0 THEN 'higher_quality_lower_conflict'
         WHEN security_goal >= 4.5 AND need_support < 4.0 THEN 'security_under_low_support'
         ELSE 'mixed_motivational_profile'
       END AS motivation_pattern,
       COUNT(*) AS n,
       ROUND(AVG(motivational_quality),3) AS quality_mean,
       ROUND(AVG(goal_conflict),3) AS conflict_mean,
       ROUND(AVG(persistence_score),3) AS persistence_mean,
       ROUND(AVG(adaptive_disengagement),3) AS disengagement_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean
FROM motivation_goals_desire
GROUP BY motivation_pattern
ORDER BY wellbeing_mean DESC;
