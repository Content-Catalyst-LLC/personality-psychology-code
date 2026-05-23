DROP TABLE IF EXISTS values_strivings_direction;

CREATE TABLE values_strivings_direction (
    person_id TEXT PRIMARY KEY,
    value_context TEXT NOT NULL,
    benevolence REAL,
    universalism REAL,
    self_direction REAL,
    achievement REAL,
    power REAL,
    security REAL,
    tradition REAL,
    stimulation REAL,
    striving_meaning REAL,
    striving_status REAL,
    striving_care REAL,
    striving_autonomy REAL,
    striving_competence REAL,
    striving_relatedness REAL,
    striving_conflict REAL,
    striving_ownership REAL,
    life_satisfaction REAL,
    self_transcendence REAL,
    self_enhancement REAL,
    openness_to_change REAL,
    conservation REAL,
    value_tension_self_transcendence_enhancement REAL,
    value_tension_openness_conservation REAL,
    value_tension_total REAL,
    striving_prosocial_orientation REAL,
    motivational_quality REAL,
    life_direction_coherence REAL
);

.mode csv
.import --skip 1 data/synthetic_values_strivings_direction.csv values_strivings_direction

.headers on
.mode column

SELECT value_context, COUNT(*) AS n,
       ROUND(AVG(self_transcendence),3) AS transcendence_mean,
       ROUND(AVG(self_enhancement),3) AS enhancement_mean,
       ROUND(AVG(openness_to_change),3) AS openness_mean,
       ROUND(AVG(conservation),3) AS conservation_mean,
       ROUND(AVG(value_tension_total),3) AS value_tension_mean,
       ROUND(AVG(motivational_quality),3) AS motivational_quality_mean,
       ROUND(AVG(striving_conflict),3) AS conflict_mean,
       ROUND(AVG(life_direction_coherence),3) AS direction_mean,
       ROUND(AVG(life_satisfaction),3) AS satisfaction_mean
FROM values_strivings_direction
GROUP BY value_context
ORDER BY satisfaction_mean DESC;

SELECT CASE
         WHEN striving_conflict >= 4.5 AND striving_ownership < 4.0 THEN 'high_conflict_low_ownership'
         WHEN striving_status >= 4.5 AND striving_meaning < 4.0 THEN 'high_status_low_meaning'
         WHEN self_transcendence >= 4.5 AND self_enhancement < 4.0 THEN 'higher_transcendence_lower_enhancement'
         WHEN self_enhancement >= 4.5 AND self_transcendence < 4.0 THEN 'higher_enhancement_lower_transcendence'
         ELSE 'mixed_direction_profile'
       END AS direction_pattern,
       COUNT(*) AS n,
       ROUND(AVG(motivational_quality),3) AS motivational_quality_mean,
       ROUND(AVG(striving_conflict),3) AS conflict_mean,
       ROUND(AVG(life_direction_coherence),3) AS direction_mean,
       ROUND(AVG(life_satisfaction),3) AS satisfaction_mean
FROM values_strivings_direction
GROUP BY direction_pattern
ORDER BY satisfaction_mean DESC;
