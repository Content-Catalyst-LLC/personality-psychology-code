DROP TABLE IF EXISTS types_traits_dimensional_models;

CREATE TABLE types_traits_dimensional_models (
    person_id TEXT PRIMARY KEY,
    assessment_context TEXT NOT NULL,
    extraversion REAL,
    agreeableness REAL,
    conscientiousness REAL,
    neuroticism REAL,
    openness REAL,
    extraversion_category TEXT,
    conscientiousness_category TEXT,
    neuroticism_category TEXT,
    profile_type TEXT,
    synthetic_cluster TEXT,
    nearest_threshold_distance REAL,
    near_threshold_boundary INTEGER,
    cluster_boundary_margin REAL,
    near_cluster_boundary INTEGER,
    dimensional_signal_strength REAL,
    information_loss_index REAL,
    well_being REAL,
    collaboration_score REAL,
    reflective_utility_score REAL
);

.mode csv
.import --skip 1 data/synthetic_types_traits_dimensional_models.csv types_traits_dimensional_models

.headers on
.mode column

SELECT profile_type,
       COUNT(*) AS n,
       ROUND(AVG(extraversion),3) AS extraversion_mean,
       ROUND(AVG(agreeableness),3) AS agreeableness_mean,
       ROUND(AVG(conscientiousness),3) AS conscientiousness_mean,
       ROUND(AVG(neuroticism),3) AS neuroticism_mean,
       ROUND(AVG(openness),3) AS openness_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean,
       ROUND(AVG(information_loss_index),3) AS information_loss_mean
FROM types_traits_dimensional_models
GROUP BY profile_type
ORDER BY n DESC;

SELECT synthetic_cluster,
       COUNT(*) AS n,
       ROUND(AVG(near_cluster_boundary),3) AS near_cluster_boundary_rate,
       ROUND(AVG(cluster_boundary_margin),3) AS boundary_margin_mean,
       ROUND(AVG(well_being),3) AS wellbeing_mean,
       ROUND(AVG(collaboration_score),3) AS collaboration_mean
FROM types_traits_dimensional_models
GROUP BY synthetic_cluster
ORDER BY n DESC;

SELECT person_id, assessment_context, profile_type, synthetic_cluster,
       nearest_threshold_distance, cluster_boundary_margin,
       information_loss_index
FROM types_traits_dimensional_models
WHERE near_threshold_boundary = 1 OR near_cluster_boundary = 1
ORDER BY nearest_threshold_distance ASC, cluster_boundary_margin ASC
LIMIT 25;
