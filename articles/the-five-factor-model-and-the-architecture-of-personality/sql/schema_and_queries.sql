DROP TABLE IF EXISTS ffm_architecture;

CREATE TABLE ffm_architecture (
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
    outcome_score REAL,
    broad_life_functioning REAL,
    relationship_functioning REAL,
    creative_engagement REAL,
    emotional_distress REAL,
    facet_profile_dispersion REAL,
    hierarchy_consistency_index REAL,
    bandwidth_fidelity_gap REAL,
    domain_facet_alignment REAL
);

.mode csv
.import --skip 1 data/synthetic_ffm_scores_for_sql.csv ffm_architecture

.headers on
.mode column

SELECT
  ROUND(AVG(extraversion_score),3) AS extraversion_mean,
  ROUND(AVG(agreeableness_score),3) AS agreeableness_mean,
  ROUND(AVG(conscientiousness_score),3) AS conscientiousness_mean,
  ROUND(AVG(neuroticism_score),3) AS neuroticism_mean,
  ROUND(AVG(openness_score),3) AS openness_mean,
  ROUND(AVG(hierarchy_consistency_index),3) AS hierarchy_consistency_mean,
  ROUND(AVG(domain_facet_alignment),3) AS domain_facet_alignment_mean
FROM ffm_architecture;

SELECT respondent_id,
       conscientiousness_score,
       orderliness_score,
       industriousness_score,
       outcome_score,
       facet_profile_dispersion,
       bandwidth_fidelity_gap
FROM ffm_architecture
ORDER BY bandwidth_fidelity_gap DESC
LIMIT 25;
