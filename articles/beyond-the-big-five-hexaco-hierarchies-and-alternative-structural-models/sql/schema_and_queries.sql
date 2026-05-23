DROP TABLE IF EXISTS alternative_structures;

CREATE TABLE alternative_structures (
    respondent_id TEXT PRIMARY KEY,
    bf_extraversion REAL,
    bf_agreeableness REAL,
    bf_conscientiousness REAL,
    bf_neuroticism REAL,
    bf_openness REAL,
    hx_honesty_humility REAL,
    hx_emotionality REAL,
    hx_extraversion REAL,
    hx_agreeableness REAL,
    hx_conscientiousness REAL,
    hx_openness REAL,
    sincerity_facet REAL,
    fairness_facet REAL,
    greed_avoidance_facet REAL,
    modesty_facet REAL,
    patience_facet REAL,
    forgiveness_facet REAL,
    anxiety_facet REAL,
    sentimentality_facet REAL,
    outcome_integrity REAL,
    outcome_interpersonal_trust REAL,
    outcome_broad_functioning REAL,
    outcome_exploitative_risk REAL,
    hexaco_increment_marker REAL,
    repartitioning_gap REAL,
    structural_comparison_index REAL,
    facet_granularity_index REAL
);

.mode csv
.import --skip 1 data/synthetic_alternative_structure_scores_for_sql.csv alternative_structures

.headers on
.mode column

SELECT
  ROUND(AVG(bf_agreeableness),3) AS bf_agreeableness_mean,
  ROUND(AVG(hx_honesty_humility),3) AS hx_honesty_humility_mean,
  ROUND(AVG(hx_agreeableness),3) AS hx_agreeableness_mean,
  ROUND(AVG(hx_emotionality),3) AS hx_emotionality_mean,
  ROUND(AVG(outcome_integrity),3) AS integrity_mean,
  ROUND(AVG(outcome_exploitative_risk),3) AS exploitative_risk_mean,
  ROUND(AVG(hexaco_increment_marker),3) AS hexaco_increment_mean,
  ROUND(AVG(repartitioning_gap),3) AS repartitioning_gap_mean
FROM alternative_structures;

SELECT respondent_id,
       hx_honesty_humility,
       bf_agreeableness,
       outcome_integrity,
       outcome_exploitative_risk,
       hexaco_increment_marker,
       structural_comparison_index
FROM alternative_structures
ORDER BY structural_comparison_index DESC
LIMIT 25;
