# Maladaptive Personality and the Border Between Normal and Clinical Structure

This directory provides reproducible research scaffolding for the article **“Maladaptive Personality and the Border Between Normal and Clinical Structure.”** It supports a dimensional workflow focused on the threshold zone where ordinary personality variation becomes rigid, pervasive, impairing, and clinically significant.

## Research focus

The central question is:

> When do ordinary personality differences become clinically meaningful maladaptive personality structure?

The scaffold examines:

- continuity between normal-range traits and maladaptive trait domains
- the distinction between trait style and disorder-level impairment
- self-functioning and interpersonal-functioning impairment
- rigidity, pervasiveness, and chronic maladaptation
- contextual stress and perceived support
- dimensional clinical liability
- exploratory threshold-zone indicators
- severity bands and dominant trait-domain profiles

## Structure

```text
data/        synthetic dataset, data dictionary, provenance notes
docs/        methods, reproducibility, responsible research use
python/      Python workflow
r/           R workflow
sql/         SQLite schema and queries
julia/       Julia summary workflow
go/          Go summary workflow
rust/        Rust summary workflow
c/           C summary workflow
cpp/         C++ summary workflow
fortran/     Fortran summary workflow
notebooks/   notebook scaffold
validation/  repository validation
outputs/     generated outputs
```

## Quick start

```bash
bash validation/run_validation.sh
python3 python/analyze_maladaptive_personality.py
Rscript r/analyze_maladaptive_personality.R
sqlite3 outputs/maladaptive_personality.sqlite < sql/schema_and_queries.sql
```

## Responsible research use

This repository is for reproducible, educational, and research-oriented analysis. It is not a diagnostic system, clinical decision-support tool, hiring or screening workflow, risk scoring system, or substitute for qualified clinical assessment.

The dataset is synthetic. It does not describe real people, patients, diagnoses, treatment programs, clinical records, workplaces, or health systems. The purpose is transparent methodological scaffolding, not claims about actual clinical populations.

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/maladaptive-personality-and-the-border-between-normal-and-clinical-structure>
