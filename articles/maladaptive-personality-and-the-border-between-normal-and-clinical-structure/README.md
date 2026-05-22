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

## Responsible Research Use

This repository provides a transparent research scaffold for studying the boundary between ordinary personality variation and maladaptive clinical structure. Its purpose is to support reproducible method development: synthetic data generation, dimensional construct modeling, threshold-zone analysis, cross-language workflow validation, and careful documentation of how traits, functioning impairment, rigidity, pervasiveness, context, and support can be represented analytically.

The synthetic dataset is included so the workflow can be inspected, replicated, and extended without relying on sensitive clinical records. Its patterns are constructed examples for testing model architecture, not empirical claims about actual people, clinical populations, treatment programs, workplaces, or health systems.

The interpretive standard is disciplined and formulation-oriented. Maladaptive personality should be understood through the convergence of trait burden, impairment in self and interpersonal functioning, rigidity, pervasiveness, contextual stress, and available support. Elevated traits alone do not establish clinical significance. Clinical significance emerges when personality structure becomes persistently inflexible, impairing, and difficult to adapt across relationships, identity, emotion, and social life.

This scaffold is best used to clarify concepts, test reproducible workflows, and support careful research design. It preserves the distinction between methodological modeling and qualified clinical judgment while treating maladaptive personality as a serious dimensional problem rather than a casual label or moral verdict.

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/maladaptive-personality-and-the-border-between-normal-and-clinical-structure>
