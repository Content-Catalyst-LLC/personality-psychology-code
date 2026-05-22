# Personality, Wellbeing, and Mental Health

This directory provides reproducible research scaffolding for the article **“Personality, Wellbeing, and Mental Health.”** It supports a personality-and-wellbeing workflow focused on Big Five traits, distress, flourishing, life satisfaction, positive affect, negative affect, meaning, coping, perceived support, stress burden, social functioning, and the two-continua view of mental health.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how personality, context, support, coping, and meaning can be modeled without reducing mental health to trait scores or treating wellbeing as simple cheerfulness.

## Research focus

The article asks a central question:

> How do enduring personality differences shape both vulnerability and flourishing through distress, coping, meaning, social support, life satisfaction, and structural context?

This directory operationalizes that question through synthetic examples that examine:

- Big Five trait associations with wellbeing and distress
- neuroticism, stress burden, rumination-like vulnerability, and distress
- extraversion, positive affect, and social vitality
- conscientiousness, self-regulation, and life management
- agreeableness, support, and relational wellbeing
- openness, meaning, reflection, and eudaimonic functioning
- two-continua mental-health profiles
- coping effectiveness and perceived support as pathways
- life context and age-band differences in wellbeing

## Directory structure

```text
personality-wellbeing-and-mental-health/
├── README.md
├── UPGRADE_MANIFEST.md
├── Makefile
├── config/
│   └── analysis_config.yml
├── data/
│   ├── synthetic_personality_wellbeing_mental_health.csv
│   ├── data_dictionary.md
│   └── provenance.md
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── responsible-research-use.md
├── python/
│   └── analyze_personality_wellbeing.py
├── r/
│   └── analyze_personality_wellbeing.R
├── sql/
│   └── schema_and_queries.sql
├── julia/
│   └── analyze_personality_wellbeing.jl
├── go/
│   └── wellbeing_summary.go
├── rust/
│   ├── Cargo.toml
│   └── src/main.rs
├── c/
│   └── wellbeing_summary.c
├── cpp/
│   └── wellbeing_summary.cpp
├── fortran/
│   └── wellbeing_summary.f90
├── notebooks/
│   └── personality_wellbeing_notebook.ipynb
├── validation/
│   ├── validate_repository.py
│   └── run_validation.sh
└── outputs/
    └── .gitkeep
```

## Data

The included dataset is synthetic. It is structured to support reproducible demonstrations of personality, wellbeing, and mental-health analysis while avoiding claims about real people, patients, clinical samples, communities, or actual diagnoses.

The data include:

- `participant_id`
- `age_band`
- `life_context`
- Big Five trait scores
- `coping_effectiveness`
- `perceived_support`
- `stress_burden`
- `positive_affect`
- `negative_affect`
- `life_satisfaction`
- `meaning_purpose`
- `wellbeing_score`
- `distress_score`
- `flourishing_score`
- `social_functioning`
- `treatment_access`
- `sleep_quality`

## Core concepts

### Mental health and wellbeing are not identical

Low symptoms and high flourishing are related but distinct. This scaffold models distress, wellbeing, and flourishing separately.

### Personality is a pathway system

Traits shape appraisal, affect, coping, support, self-regulation, routines, meaning, and environment selection. They do not determine mental health alone.

### Context matters

Stress burden, treatment access, perceived support, structural security, and social context shape whether trait tendencies become protective, harmful, or neutral.

### Responsible analysis requires dignity

Personality language should not be used to blame people for suffering, diagnose character, or reduce distress to individual disposition.

## Quick start

Run the validation script:

```bash
bash validation/run_validation.sh
```

Run the Python workflow:

```bash
python3 python/analyze_personality_wellbeing.py
```

Run the R workflow:

```bash
Rscript r/analyze_personality_wellbeing.R
```

Run SQL examples with SQLite:

```bash
sqlite3 outputs/personality_wellbeing.sqlite < sql/schema_and_queries.sql
```

Run the Makefile workflow:

```bash
make validate
make python
```

## Outputs

Generated outputs are written to `outputs/`, including:

- age-band summaries
- life-context summaries
- trait-wellbeing correlation matrices
- two-continua mental-health profile summaries
- distress vulnerability indices
- flourishing capacity indices
- wellbeing, distress, and flourishing model outputs
- validation reports

## Responsible Research Use

This repository is designed for reproducible, research-oriented analysis of personality, wellbeing, and mental health. Its purpose is to support careful thinking about traits, vulnerability, coping, flourishing, distress, meaning, support, and social context.

The examples use synthetic data so the workflows can be inspected, adapted, and extended without relying on private mental-health records or making claims about actual persons, patients, communities, diagnoses, or care systems. The emphasis is on transparent methods, reproducible code, and disciplined interpretation.

Personality-wellbeing analysis should be handled with particular care. Apparent differences in wellbeing, distress, flourishing, coping, or support may reflect trauma, poverty, discrimination, disability, caregiving burden, isolation, institutional violence, illness, social support, treatment access, cultural norms, or measurement design rather than stable traits alone.

The strongest use of this scaffold is supportive and systems-aware: examining how personality and lived conditions interact, distinguishing distress from flourishing, clarifying pathways without pathologizing ordinary difference, and designing supports that preserve dignity.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/personality-wellbeing-and-mental-health>
