# Data Dictionary

## Dataset: `synthetic_trait_items.csv`

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `c1`–`c6` | Synthetic conscientiousness item responses |
| `e1`–`e6` | Synthetic extraversion item responses |
| `n1`–`n6` | Synthetic neuroticism item responses |
| `conscientiousness_score` | Synthetic mean conscientiousness score |
| `extraversion_score` | Synthetic mean extraversion score |
| `neuroticism_score` | Synthetic mean neuroticism score |
| `self_report_consistency_index` | Synthetic marker of within-scale response consistency |
| `trait_observation_alignment` | Synthetic marker of how well trait scores align with repeated-state evidence |

## Dataset: `synthetic_state_observations.csv`

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `occasion` | Observation occasion |
| `situation_type` | Synthetic situation label |
| `state_extraversion` | Momentary state extraversion rating |
| `state_conscientiousness` | Momentary state conscientiousness rating |
| `state_neuroticism` | Momentary state neuroticism rating |
| `situational_activation` | Synthetic situation activation score |
| `situational_constraint` | Synthetic situation constraint score |

## Dataset: `synthetic_trait_state_summary_for_sql.csv`

Compact person-level summary for SQL examples.

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `conscientiousness_score` | Synthetic trait score |
| `extraversion_score` | Synthetic trait score |
| `neuroticism_score` | Synthetic trait score |
| `mean_state_conscientiousness` | Average repeated-state conscientiousness |
| `sd_state_conscientiousness` | Within-person state conscientiousness variability |
| `mean_state_extraversion` | Average repeated-state extraversion |
| `sd_state_extraversion` | Within-person state extraversion variability |
| `mean_state_neuroticism` | Average repeated-state neuroticism |
| `sd_state_neuroticism` | Within-person state neuroticism variability |
| `n_observations` | Number of repeated-state observations |
| `trait_state_alignment_index` | Synthetic trait/state agreement marker |
| `state_variability_index` | Synthetic within-person variability marker |
| `person_situation_sensitivity_index` | Synthetic person-situation sensitivity marker |
| `aggregation_reliability_index` | Synthetic repeated-measure aggregation marker |

The datasets are synthetic and not representative of real respondents, clients, patients, students, workers, communities, cultures, organizations, or institutions.
