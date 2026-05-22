# Personality, Culture, and the Problem of Universality

This directory provides reproducible research scaffolding for the article **“Personality, Culture, and the Problem of Universality.”** It supports a cross-cultural personality psychology workflow focused on Big Five / Big Six trait structure, universality claims, measurement fit, cultural context, and behavioral manifestation.

The repository is designed as an educational and research-oriented companion to the article. It demonstrates how cross-cultural personality questions can be approached with transparent data documentation, reproducible scripts, language-agnostic analysis patterns, and responsible interpretation.

## Research focus

The article asks a central theoretical question:

> When personality psychology describes enduring traits, is it identifying structures that are genuinely human-wide, or is it partly exporting historically local vocabularies, languages, and assumptions about personhood?

This directory operationalizes that question through synthetic examples that examine:

- Cross-cultural trait summaries
- Big Five and Big Six comparison
- Within-group trait correlation structures
- Approximate replicability across cultural groups
- Trait-context interaction models
- Measurement-fit thinking and invariance caution
- The distinction between broad recurrence and strict universality
- Responsible interpretation of cross-cultural personality evidence

## Directory structure

```text
personality-culture-and-the-problem-of-universality/
├── README.md
├── UPGRADE_MANIFEST.md
├── Makefile
├── config/
│   └── analysis_config.yml
├── data/
│   ├── synthetic_personality_culture_universality.csv
│   ├── data_dictionary.md
│   └── provenance.md
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── responsible-use.md
├── python/
│   └── analyze_personality_culture_universality.py
├── r/
│   └── analyze_personality_culture_universality.R
├── sql/
│   └── schema_and_queries.sql
├── julia/
│   └── analyze_personality_culture_universality.jl
├── go/
│   └── matrix_similarity.go
├── rust/
│   ├── Cargo.toml
│   └── src/main.rs
├── c/
│   └── trait_summary.c
├── cpp/
│   └── trait_summary.cpp
├── fortran/
│   └── trait_summary.f90
├── notebooks/
│   └── personality_culture_universality_notebook.ipynb
├── validation/
│   ├── validate_repository.py
│   └── run_validation.sh
└── outputs/
    └── .gitkeep
```

## Data

The included dataset is synthetic. It is structured to support reproducible demonstrations of cross-cultural personality analysis while avoiding claims about real populations.

The data include:

- `culture_group`
- `openness`
- `conscientiousness`
- `extraversion`
- `agreeableness`
- `neuroticism`
- `honesty_humility`
- `context_collectivism`
- `behavioral_manifestation`

These fields allow the examples to model both trait structure and context-sensitive expression.

## Core concepts

### Broad recurrence

Broad recurrence means that trait-like dimensions appear repeatedly across societies at a high level of abstraction.

### Strong universality

Strong universality requires stronger evidence: comparable latent structure, comparable item functioning, comparable scale meaning, and comparable behavioral correlates across cultural groups.

### Measurement fit

Cross-cultural personality models require attention to whether translated items, scales, and factors are measuring the same constructs in comparable ways.

### Cultural manifestation

A trait can be structurally similar across groups but behaviorally expressed in different ways because local norms shape what counts as assertive, dutiful, modest, sociable, emotionally expressive, or responsible.

## Quick start

Run the validation script:

```bash
bash validation/run_validation.sh
```

Run the Python workflow:

```bash
python3 python/analyze_personality_culture_universality.py
```

Run the R workflow:

```bash
Rscript r/analyze_personality_culture_universality.R
```

Run SQL examples with SQLite:

```bash
sqlite3 outputs/personality_culture_universality.sqlite < sql/schema_and_queries.sql
```

Run the Makefile workflow:

```bash
make validate
make python
```

## Outputs

Generated outputs are written to `outputs/`, including:

- group summary CSV files
- trait correlation matrices
- matrix similarity estimates
- simple trait-context model outputs
- validation reports

## Responsible use

This repository is not a clinical, diagnostic, employment-screening, hiring, personality-testing, workplace-selection, or population-ranking tool. It is a research scaffold for thinking carefully about cross-cultural personality structure and measurement. The examples use synthetic data only.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/personality-culture-and-the-problem-of-universality>
