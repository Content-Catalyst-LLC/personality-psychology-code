DROP TABLE IF EXISTS trait_hierarchies;

CREATE TABLE trait_hierarchies (
    respondent_id TEXT PRIMARY KEY,
    extraversion_score REAL,
    agreeableness_score REAL,
    conscientiousness_score REAL,
    neuroticism_score REAL,
    openness_score REAL,
    sociability_score REAL,
    assertiveness_score REAL,
    compassion_score REAL,
    politeness_score REAL,
    orderliness_score REAL,
    industriousness_score REAL,
    anxiety_score REAL,
    volatility_score REAL,
    aesthetics_score REAL,
    intellect_score REAL,
    broad_life_functioning REAL,
    focused_reliability_outcome REAL,
    creative_engagement_outcome REAL,
    bandwidth_fidelity_gap REAL,
    facet_profile_dispersion REAL,
    hierarchy_consistency_index REAL
);

.mode csv
.import --skip 1 data/synthetic_hierarchical_trait_scores_for_sql.csv trait_hierarchies

.headers on
.mode column

SELECT
  ROUND(AVG(extraversion_score),3) AS extraversion_mean,
  ROUND(AVG(agreeableness_score),3) AS agreeableness_mean,
  ROUND(AVG(conscientiousness_score),3) AS conscientiousness_mean,
  ROUND(AVG(neuroticism_score),3) AS neuroticism_mean,
  ROUND(AVG(openness_score),3) AS openness_mean,
  ROUND(AVG(facet_profile_dispersion),3) AS facet_dispersion_mean,
  ROUND(AVG(hierarchy_consistency_index),3) AS hierarchy_consistency_mean
FROM trait_hierarchies;

SELECT respondent_id,
       conscientiousness_score,
       orderliness_score,
       industriousness_score,
       focused_reliability_outcome,
       facet_profile_dispersion
FROM trait_hierarchies
ORDER BY facet_profile_dispersion DESC
LIMIT 25;
