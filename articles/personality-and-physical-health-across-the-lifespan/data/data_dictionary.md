# Data Dictionary

Dataset: `synthetic_personality_physical_health_lifespan.csv`

This is a synthetic dataset for reproducible educational examples. Values are generated to resemble plausible lifespan personality-health structure but do not describe real people, patients, communities, clinical records, or health systems.

| Column | Type | Description |
|---|---:|---|
| `person_id` | string | Synthetic person identifier |
| `wave` | integer | Synthetic longitudinal wave |
| `age` | numeric | Synthetic age at observation |
| `age_band` | string | Synthetic life-stage category |
| `life_context` | string | Synthetic structural / health-opportunity context |
| `extraversion` | numeric | Synthetic Big Five extraversion score |
| `agreeableness` | numeric | Synthetic Big Five agreeableness score |
| `conscientiousness` | numeric | Synthetic Big Five conscientiousness score |
| `neuroticism` | numeric | Synthetic Big Five neuroticism score |
| `openness` | numeric | Synthetic Big Five openness score |
| `emotional_stability` | numeric | Synthetic emotional stability score |
| `perceived_support` | numeric | Synthetic perceived social support score |
| `exercise` | numeric | Synthetic activity / movement behavior score |
| `sleep_quality` | numeric | Synthetic sleep quality score |
| `smoking_risk` | numeric | Synthetic smoking or nicotine-related risk score |
| `alcohol_risk` | numeric | Synthetic alcohol-related risk score |
| `medication_adherence` | numeric | Synthetic treatment adherence / care-follow-through score |
| `stress_burden` | numeric | Synthetic chronic stress burden score |
| `physical_health_score` | numeric | Synthetic overall physical health score |
| `functional_ability` | numeric | Synthetic functional ability score |
| `chronic_condition_burden` | numeric | Synthetic chronic condition burden score |

## Important caution

The dataset is not representative of any actual person, patient population, disease group, health system, country, or community. It should be used only to test code and illustrate analysis patterns.
