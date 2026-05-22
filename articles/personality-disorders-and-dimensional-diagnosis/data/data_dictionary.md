# Data Dictionary

Dataset: `synthetic_personality_disorders_dimensional_diagnosis.csv`

This is a synthetic dataset for reproducible educational examples. Values are generated to resemble plausible dimensional personality-pathology structure but do not describe real people, patients, clinical groups, diagnoses, treatment programs, or health systems.

| Column | Type | Description |
|---|---:|---|
| `participant_id` | string | Synthetic person identifier |
| `clinical_context` | string | Synthetic clinical / structural context label |
| `negative_affectivity` | numeric | Synthetic maladaptive trait domain: negative affectivity |
| `detachment` | numeric | Synthetic maladaptive trait domain: detachment |
| `antagonism` | numeric | Synthetic maladaptive trait domain: antagonism |
| `disinhibition` | numeric | Synthetic maladaptive trait domain: disinhibition |
| `psychoticism` | numeric | Synthetic maladaptive trait domain: psychoticism |
| `anankastia` | numeric | Synthetic maladaptive trait domain: rigid perfectionism / compulsive control |
| `identity_impairment` | numeric | Synthetic impairment in identity functioning |
| `self_direction_impairment` | numeric | Synthetic impairment in self-direction |
| `empathy_impairment` | numeric | Synthetic impairment in empathy |
| `intimacy_impairment` | numeric | Synthetic impairment in intimacy |
| `self_functioning` | numeric | Synthetic composite of identity and self-direction impairment |
| `interpersonal_functioning` | numeric | Synthetic composite of empathy and intimacy impairment |
| `functioning_impairment` | numeric | Synthetic overall personality-functioning impairment |
| `maladaptive_trait_burden` | numeric | Synthetic average maladaptive trait-domain burden |
| `severity_trait_interaction` | numeric | Synthetic interaction between functioning impairment and trait burden |
| `borderline_pattern_indicator` | numeric | Synthetic borderline-pattern feature indicator |
| `pd_severity` | numeric | Synthetic personality disorder severity score |
| `risk_level` | numeric | Synthetic risk / clinical planning score |
| `treatment_engagement` | numeric | Synthetic treatment engagement / continuity score |
| `perceived_support` | numeric | Synthetic perceived support score |

## Important caution

The dataset is not representative of any actual person, patient population, diagnostic category, treatment program, or clinical system. It should be used only to test code and illustrate analysis patterns.
