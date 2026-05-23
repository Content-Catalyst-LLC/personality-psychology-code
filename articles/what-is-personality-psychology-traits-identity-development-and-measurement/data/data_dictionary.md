# Data Dictionary

## Dataset: `synthetic_personality_items.csv`

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `item1`–`item60` | Synthetic broad personality item pool |
| `c1`–`c6` | Synthetic conscientiousness item responses |
| `e1`–`e6` | Synthetic extraversion item responses |
| `n1`–`n6` | Synthetic neuroticism item responses |
| `conscientiousness_score` | Synthetic mean conscientiousness score |
| `extraversion_score` | Synthetic mean extraversion score |
| `neuroticism_score` | Synthetic mean neuroticism score |
| `identity_coherence` | Synthetic outcome representing identity coherence |
| `life_satisfaction` | Synthetic outcome representing wellbeing |
| `social_functioning` | Synthetic outcome representing social functioning |
| `developmental_integration` | Synthetic outcome representing life-course integration |
| `measurement_reliability_index` | Synthetic marker of item/scale consistency |
| `identity_trait_alignment_index` | Synthetic marker of alignment between trait pattern and identity-linked outcomes |
| `person_situation_sensitivity_index` | Synthetic marker of person-situation responsiveness |
| `responsible_interpretation_index` | Synthetic marker for cautious, evidence-proportionate interpretation |

## Dataset: `synthetic_person_situation_observations.csv`

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `occasion` | Observation occasion |
| `situation_type` | Synthetic situation label |
| `behavior_score` | Synthetic behavior criterion |
| `trait_score` | Synthetic trait predictor |
| `situation_strength` | Synthetic situation-strength predictor |
| `trait_x_situation` | Interaction term |
| `observed_regulation` | Synthetic state/regulation observation |
| `contextual_constraint` | Synthetic situation constraint score |

## Dataset: `synthetic_personality_summary_for_sql.csv`

Compact person-level summary for SQL examples.

The datasets are synthetic and not representative of real respondents, clients, patients, students, workers, communities, cultures, organizations, languages, institutions, or historical populations.
