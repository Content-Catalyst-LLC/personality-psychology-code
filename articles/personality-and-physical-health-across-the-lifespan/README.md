# Personality and Physical Health Across the Lifespan

This directory provides reproducible research scaffolding for the article **“Personality and Physical Health Across the Lifespan.”** It supports a lifespan personality-health workflow focused on Big Five traits, health behavior, stress burden, treatment adherence, functional ability, healthy ageing, and the structural conditions that shape physical-health trajectories.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how personality, behavior, stress, social support, care access, ageing, and health inequality can be modeled without reducing physical health to traits alone.

## Research focus

The article asks a central question:

> How do enduring personality differences become embodied across the lifespan through health behavior, stress reactivity, medical adherence, social support, ageing, functional ability, and unequal access to care?

This directory operationalizes that question through synthetic examples that examine:

- Big Five trait associations with physical health
- conscientiousness, routine, and health-protective behavior
- neuroticism, stress burden, and emotional reactivity
- healthy neuroticism as a conditional trait configuration
- exercise, sleep, substance risk, and treatment adherence
- social support and stress vulnerability
- healthy ageing and functional ability
- chronic-condition burden across repeated waves
- structural context and unequal health opportunity

## Directory structure

```text
personality-and-physical-health-across-the-lifespan/
├── README.md
├── UPGRADE_MANIFEST.md
├── Makefile
├── config/
│   └── analysis_config.yml
├── data/
│   ├── synthetic_personality_physical_health_lifespan.csv
│   ├── data_dictionary.md
│   └── provenance.md
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── responsible-research-use.md
├── python/
│   └── analyze_personality_physical_health.py
├── r/
│   └── analyze_personality_physical_health.R
├── sql/
│   └── schema_and_queries.sql
├── julia/
│   └── analyze_personality_physical_health.jl
├── go/
│   └── health_summary.go
├── rust/
│   ├── Cargo.toml
│   └── src/main.rs
├── c/
│   └── health_summary.c
├── cpp/
│   └── health_summary.cpp
├── fortran/
│   └── health_summary.f90
├── notebooks/
│   └── personality_physical_health_notebook.ipynb
├── validation/
│   ├── validate_repository.py
│   └── run_validation.sh
└── outputs/
    └── .gitkeep
```

## Data

The included dataset is synthetic. It is structured to support reproducible demonstrations of lifespan personality-health analysis while avoiding claims about real patients, real clinical records, real populations, real health systems, or actual mortality / disease outcomes.

The data include:

- `person_id`
- `wave`
- `age`
- `age_band`
- `life_context`
- Big Five trait scores
- `emotional_stability`
- `perceived_support`
- `exercise`
- `sleep_quality`
- `smoking_risk`
- `alcohol_risk`
- `medication_adherence`
- `stress_burden`
- `physical_health_score`
- `functional_ability`
- `chronic_condition_burden`

## Core concepts

### Health is patterned over time

Physical health is shaped by repeated behavior, care access, stress exposure, social support, and bodily ageing. Personality matters because it helps stabilize those repeated pathways.

### Conscientiousness is a health-protective pathway

Conscientiousness often supports routine, adherence, prevention, safer behavior, and long-horizon self-regulation.

### Neuroticism is conditional

Neuroticism may increase stress burden and physiological strain, but when paired with conscientiousness it can sometimes support vigilance, monitoring, and preventive action.

### Functional ability is person-plus-environment

Healthy ageing depends on personality and physical condition, but also on caregiving, housing, access, mobility, infrastructure, and public systems.

## Quick start

Run the validation script:

```bash
bash validation/run_validation.sh
```

Run the Python workflow:

```bash
python3 python/analyze_personality_physical_health.py
```

Run the R workflow:

```bash
Rscript r/analyze_personality_physical_health.R
```

Run SQL examples with SQLite:

```bash
sqlite3 outputs/personality_physical_health.sqlite < sql/schema_and_queries.sql
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
- trait-health correlation matrices
- health behavior indices
- stress vulnerability indices
- physical health and functional ability model outputs
- validation reports

## Responsible Research Use

This repository is designed for reproducible, research-oriented analysis of personality and physical health across the lifespan. Its purpose is to support careful thinking about traits, health behavior, stress burden, support, adherence, ageing, functional ability, and the structural conditions that shape health trajectories.

The examples use synthetic data so the workflows can be inspected, adapted, and extended without relying on private medical records or making claims about actual people, patients, communities, or health systems. The emphasis is on transparent methods, reproducible code, and disciplined interpretation.

Personality-health analysis should be handled with particular care. Apparent differences in physical health may reflect biology, environment, care access, disability, occupational hazard, discrimination, poverty, medical mistrust, food systems, pollution exposure, caregiving burden, public policy, or measurement design rather than stable traits alone.

The strongest use of this scaffold is supportive and systems-aware: examining how personality and health systems interact, clarifying behavioral and stress-related pathways, and designing care supports without blaming people for illness or reducing health inequality to individual disposition.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/personality-and-physical-health-across-the-lifespan>
