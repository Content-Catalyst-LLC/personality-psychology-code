DROP TABLE IF EXISTS behavior_genetics_personality;

CREATE TABLE behavior_genetics_personality (
    pair_id TEXT PRIMARY KEY,
    zygosity TEXT NOT NULL,
    genetic_relatedness REAL,
    twin1_trait REAL,
    twin2_trait REAL,
    twin1_temperament_reactivity REAL,
    twin2_temperament_reactivity REAL,
    twin1_effortful_control REAL,
    twin2_effortful_control REAL,
    family_stress REAL,
    social_support REAL,
    socioeconomic_security REAL,
    educational_stability REAL,
    shared_environment_index REAL,
    nonshared_environment_index REAL,
    trait_mean REAL,
    trait_difference REAL,
    gxe_marker REAL,
    rge_marker REAL,
    developmental_context_score REAL
);

.mode csv
.import --skip 1 data/synthetic_personality_twin_data.csv behavior_genetics_personality

.headers on
.mode column

SELECT zygosity,
       COUNT(*) AS n_pairs,
       ROUND(AVG(trait_mean),3) AS trait_mean,
       ROUND(AVG(trait_difference),3) AS trait_difference_mean,
       ROUND(AVG(family_stress),3) AS family_stress_mean,
       ROUND(AVG(social_support),3) AS social_support_mean,
       ROUND(AVG(socioeconomic_security),3) AS socioeconomic_security_mean,
       ROUND(AVG(nonshared_environment_index),3) AS nonshared_environment_mean,
       ROUND(AVG(gxe_marker),3) AS gxe_marker_mean,
       ROUND(AVG(rge_marker),3) AS rge_marker_mean
FROM behavior_genetics_personality
GROUP BY zygosity
ORDER BY zygosity;

SELECT pair_id, zygosity, trait_difference, family_stress, social_support,
       socioeconomic_security, nonshared_environment_index, gxe_marker
FROM behavior_genetics_personality
ORDER BY trait_difference DESC
LIMIT 25;
