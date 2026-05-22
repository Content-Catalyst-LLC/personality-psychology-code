# Personality Disorders and Dimensional Diagnosis

This directory provides reproducible research scaffolding for the article **“Personality Disorders and Dimensional Diagnosis.”** It supports a dimensional personality-pathology workflow focused on severity, maladaptive trait domains, self-functioning impairment, interpersonal-functioning impairment, risk indicators, treatment engagement, diagnostic thresholds, and the shift from categorical personality disorder labels toward structured clinical formulation.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how severity, maladaptive traits, DSM-5 AMPD-style criteria, ICD-11-style trait qualifiers, risk, and clinical context can be modeled without turning dimensional diagnosis into an automated diagnostic system.

## Research focus

The article asks a central question:

> How can personality disorder diagnosis move beyond rigid categories toward a dimensional model that represents severity, maladaptive traits, self-functioning, interpersonal functioning, and clinical context more faithfully?

This directory operationalizes that question through synthetic examples that examine:

- dimensional personality disorder severity
- maladaptive trait domains
- self-functioning and interpersonal-functioning impairment
- identity, self-direction, empathy, and intimacy impairment
- DSM-5 Alternative Model for Personality Disorders-style modeling
- ICD-11-style severity and trait-qualifier framing
- borderline pattern indicators as a continuity construct
- risk level as distinct from diagnostic severity
- treatment engagement as contextual and relational rather than purely trait-based
- severity bands, dominant trait domains, and dimensional profile summaries

## Directory structure

```text
personality-disorders-and-dimensional-diagnosis/
├── README.md
├── UPGRADE_MANIFEST.md
├── Makefile
├── config/
│   └── analysis_config.yml
├── data/
│   ├── synthetic_personality_disorders_dimensional_diagnosis.csv
│   ├── data_dictionary.md
│   └── provenance.md
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── responsible-research-use.md
├── python/
│   └── analyze_dimensional_personality_disorders.py
├── r/
│   └── analyze_dimensional_personality_disorders.R
├── sql/
│   └── schema_and_queries.sql
├── julia/
│   └── analyze_dimensional_personality_disorders.jl
├── go/
│   └── dimensional_pd_summary.go
├── rust/
│   ├── Cargo.toml
│   └── src/main.rs
├── c/
│   └── dimensional_pd_summary.c
├── cpp/
│   └── dimensional_pd_summary.cpp
├── fortran/
│   └── dimensional_pd_summary.f90
├── notebooks/
│   └── dimensional_personality_disorders_notebook.ipynb
├── validation/
│   ├── validate_repository.py
│   └── run_validation.sh
└── outputs/
    └── .gitkeep
```

## Data

The included dataset is synthetic. It is structured to support reproducible demonstrations of dimensional personality-disorder analysis while avoiding claims about real patients, real diagnoses, clinical records, treatment populations, or health systems.

The data include:

- `participant_id`
- `clinical_context`
- `negative_affectivity`
- `detachment`
- `antagonism`
- `disinhibition`
- `psychoticism`
- `anankastia`
- `identity_impairment`
- `self_direction_impairment`
- `empathy_impairment`
- `intimacy_impairment`
- `self_functioning`
- `interpersonal_functioning`
- `functioning_impairment`
- `maladaptive_trait_burden`
- `borderline_pattern_indicator`
- `pd_severity`
- `risk_level`
- `treatment_engagement`
- `perceived_support`

## Core concepts

### Diagnosis can be dimensional and clinically serious

A dimensional model does not make personality disorder less real. It represents disorder through severity, impairment, trait configuration, and clinical context.

### Severity and style are distinct

Severity describes how deeply personality functioning is impaired. Style describes the maladaptive trait configuration through which impairment appears.

### Self and interpersonal functioning are clinical core

Identity, self-direction, empathy, and intimacy are central to contemporary dimensional models because personality pathology is deeply tied to selfhood and relationship.

### Thresholds are secondary

Clinical or administrative thresholds may still be used, but they sit on top of underlying dimensional liability rather than defining the structure by themselves.

## Quick start

Run the validation script:

```bash
bash validation/run_validation.sh
```

Run the Python workflow:

```bash
python3 python/analyze_dimensional_personality_disorders.py
```

Run the R workflow:

```bash
Rscript r/analyze_dimensional_personality_disorders.R
```

Run SQL examples with SQLite:

```bash
sqlite3 outputs/dimensional_personality_disorders.sqlite < sql/schema_and_queries.sql
```

Run the Makefile workflow:

```bash
make validate
make python
```

## Outputs

Generated outputs are written to `outputs/`, including:

- severity-band summaries
- dominant-trait-domain summaries
- clinical-context summaries
- trait and functioning correlation matrices
- dimensional severity model outputs
- risk and treatment-engagement model outputs
- validation reports

## Responsible Research Use

This repository is designed for reproducible, research-oriented analysis of dimensional personality disorder diagnosis. Its purpose is to support careful thinking about severity, traits, self-functioning, interpersonal functioning, risk, treatment engagement, and clinical context.

The examples use synthetic data so the workflows can be inspected, adapted, and extended without relying on private clinical records or making claims about actual patients, diagnoses, therapists, treatment programs, or health systems. The emphasis is on transparent methods, reproducible code, and disciplined interpretation.

Dimensional personality-disorder analysis should be handled with particular care. Apparent differences in severity, functioning, trait expression, risk, or treatment engagement may reflect trauma history, disability, social exclusion, substance use, mood conditions, neurodevelopmental conditions, cultural context, clinical setting, treatment access, stigma, clinician bias, or measurement design rather than personality structure alone.

The strongest use of this scaffold is educational and formulation-oriented: examining how dimensional models organize severity and trait information, distinguishing clinical description from moral judgment, and supporting better conceptual clarity without automating diagnosis.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/personality-disorders-and-dimensional-diagnosis>
