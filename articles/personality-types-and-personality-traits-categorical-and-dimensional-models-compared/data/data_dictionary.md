# Data Dictionary

Dataset: `synthetic_types_traits_dimensional_models.csv`

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `assessment_context` | Synthetic context in which type/trait representation is being examined |
| `extraversion` | Continuous trait score for sociability/assertive energy |
| `agreeableness` | Continuous trait score for cooperation, warmth, and interpersonal accommodation |
| `conscientiousness` | Continuous trait score for order, responsibility, and sustained regulation |
| `neuroticism` | Continuous trait score for negative emotionality and stress reactivity |
| `openness` | Continuous trait score for curiosity, imagination, and intellectual/aesthetic exploration |
| `extraversion_category` | Thresholded low/moderate/high category derived from extraversion |
| `conscientiousness_category` | Thresholded low/moderate/high category derived from conscientiousness |
| `neuroticism_category` | Thresholded low/moderate/high category derived from neuroticism |
| `profile_type` | Coarse categorical profile label derived from multiple trait thresholds |
| `synthetic_cluster` | Synthetic person-centered profile group used for demonstration |
| `nearest_threshold_distance` | Distance to the nearest low/moderate/high trait threshold |
| `near_threshold_boundary` | Indicator for cases near a threshold boundary |
| `cluster_boundary_margin` | Difference between nearest and second-nearest synthetic profile distance |
| `near_cluster_boundary` | Indicator for people close to a profile boundary |
| `dimensional_signal_strength` | Mean standardized distance from trait midpoints |
| `information_loss_index` | Synthetic index representing compression after categorical summarization |
| `well_being` | Synthetic wellbeing outcome |
| `collaboration_score` | Synthetic collaboration outcome |
| `reflective_utility_score` | Synthetic score representing professional/educational discussion value |

The dataset is synthetic and not representative of actual people, workers, students, clients, teams, organizations, schools, communities, cultures, or institutions.
