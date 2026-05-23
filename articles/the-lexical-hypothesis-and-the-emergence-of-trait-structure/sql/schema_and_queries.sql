DROP TABLE IF EXISTS lexical_structure;

CREATE TABLE lexical_structure (
    respondent_id TEXT PRIMARY KEY,
    sociable_cluster_score REAL,
    reliable_cluster_score REAL,
    compassionate_cluster_score REAL,
    anxious_cluster_score REAL,
    imaginative_cluster_score REAL,
    social_reliability_outcome REAL,
    interpersonal_trust_outcome REAL,
    expressive_engagement_outcome REAL,
    lexical_visibility_index REAL,
    lexical_abundance_index REAL,
    structural_centrality_index REAL,
    descriptor_redundancy_index REAL,
    cross_language_caution_index REAL
);

.mode csv
.import --skip 1 data/synthetic_lexical_scores_for_sql.csv lexical_structure

.headers on
.mode column

SELECT
  ROUND(AVG(sociable_cluster_score),3) AS sociable_mean,
  ROUND(AVG(reliable_cluster_score),3) AS reliable_mean,
  ROUND(AVG(compassionate_cluster_score),3) AS compassionate_mean,
  ROUND(AVG(anxious_cluster_score),3) AS anxious_mean,
  ROUND(AVG(imaginative_cluster_score),3) AS imaginative_mean,
  ROUND(AVG(lexical_abundance_index),3) AS lexical_abundance_mean,
  ROUND(AVG(structural_centrality_index),3) AS structural_centrality_mean,
  ROUND(AVG(cross_language_caution_index),3) AS cross_language_caution_mean
FROM lexical_structure;

SELECT respondent_id,
       reliable_cluster_score,
       compassionate_cluster_score,
       social_reliability_outcome,
       interpersonal_trust_outcome,
       descriptor_redundancy_index,
       structural_centrality_index
FROM lexical_structure
ORDER BY structural_centrality_index DESC
LIMIT 25;
