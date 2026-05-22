DROP TABLE IF EXISTS mbti_typology_vs_traits;

CREATE TABLE mbti_typology_vs_traits (
    person_id TEXT PRIMARY KEY,
    assessment_context TEXT NOT NULL,
    latent_ei REAL,
    latent_sn REAL,
    latent_tf REAL,
    latent_jp REAL,
    observed_ei REAL,
    observed_sn REAL,
    observed_tf REAL,
    observed_jp REAL,
    retest_ei REAL,
    retest_sn REAL,
    retest_tf REAL,
    retest_jp REAL,
    ei_letter TEXT,
    sn_letter TEXT,
    tf_letter TEXT,
    jp_letter TEXT,
    type_code TEXT,
    retest_type_code TEXT,
    type_changed_on_retest INTEGER,
    min_absolute_distance_to_boundary REAL,
    near_boundary INTEGER,
    continuous_signal_strength REAL,
    boundary_risk_score REAL,
    information_loss_index REAL,
    collaboration_score REAL,
    reflective_utility_score REAL
);

.mode csv
.import --skip 1 data/synthetic_mbti_typology_vs_traits.csv mbti_typology_vs_traits

.headers on
.mode column

SELECT type_code,
       COUNT(*) AS n,
       ROUND(AVG(type_changed_on_retest),3) AS type_change_rate,
       ROUND(AVG(near_boundary),3) AS near_boundary_rate,
       ROUND(AVG(boundary_risk_score),3) AS boundary_risk_mean,
       ROUND(AVG(information_loss_index),3) AS information_loss_mean,
       ROUND(AVG(collaboration_score),3) AS collaboration_mean
FROM mbti_typology_vs_traits
GROUP BY type_code
ORDER BY n DESC;

SELECT assessment_context,
       COUNT(*) AS n,
       ROUND(AVG(near_boundary),3) AS near_boundary_rate,
       ROUND(AVG(type_changed_on_retest),3) AS type_change_rate,
       ROUND(AVG(boundary_risk_score),3) AS boundary_risk_mean,
       ROUND(AVG(information_loss_index),3) AS information_loss_mean,
       ROUND(AVG(reflective_utility_score),3) AS reflective_utility_mean
FROM mbti_typology_vs_traits
GROUP BY assessment_context
ORDER BY type_change_rate DESC;

SELECT person_id, assessment_context, type_code, retest_type_code,
       min_absolute_distance_to_boundary, boundary_risk_score, information_loss_index
FROM mbti_typology_vs_traits
WHERE near_boundary = 1
ORDER BY min_absolute_distance_to_boundary ASC
LIMIT 25;
