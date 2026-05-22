# Data Dictionary

Dataset: `synthetic_mbti_typology_vs_traits.csv`

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `assessment_context` | Synthetic context in which typology language is being examined |
| `latent_ei` | Continuous latent Extraversion–Introversion dimension |
| `latent_sn` | Continuous latent Sensing–Intuition dimension |
| `latent_tf` | Continuous latent Thinking–Feeling dimension |
| `latent_jp` | Continuous latent Judging–Perceiving dimension |
| `observed_ei` | Observed EI score after measurement fluctuation |
| `observed_sn` | Observed SN score after measurement fluctuation |
| `observed_tf` | Observed TF score after measurement fluctuation |
| `observed_jp` | Observed JP score after measurement fluctuation |
| `retest_ei` | Retest EI score after additional fluctuation |
| `retest_sn` | Retest SN score after additional fluctuation |
| `retest_tf` | Retest TF score after additional fluctuation |
| `retest_jp` | Retest JP score after additional fluctuation |
| `ei_letter` | Dichotomous assignment from observed EI score |
| `sn_letter` | Dichotomous assignment from observed SN score |
| `tf_letter` | Dichotomous assignment from observed TF score |
| `jp_letter` | Dichotomous assignment from observed JP score |
| `type_code` | Four-letter MBTI-style type code |
| `retest_type_code` | Four-letter retest type code |
| `type_changed_on_retest` | Whether the type code changed under retest fluctuation |
| `min_absolute_distance_to_boundary` | Closest observed score distance to a dichotomous threshold |
| `near_boundary` | Indicator for cases close to at least one threshold |
| `continuous_signal_strength` | Mean absolute observed dimensional score |
| `boundary_risk_score` | Higher values indicate greater threshold fragility |
| `information_loss_index` | Synthetic index representing information lost by categorical compression |
| `collaboration_score` | Synthetic outcome predicted from continuous dimensions |
| `reflective_utility_score` | Synthetic outcome representing potential discussion/reflection usefulness |

The dataset is synthetic and not representative of actual MBTI users, employees, students, clients, teams, organizations, schools, communities, cultures, or institutions.
