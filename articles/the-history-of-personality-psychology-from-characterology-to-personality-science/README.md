# The History of Personality Psychology: From Characterology to Personality Science

This directory provides reproducible research scaffolding for the article **“The History of Personality Psychology: From Characterology to Personality Science.”** It supports a professional workflow focused on the transition from typological characterology to dimensional personality science, including item pools, latent structure, reliability, longitudinal stability, person-situation interaction, measurement-invariance cautions, and responsible interpretation.

The scaffold treats the history of personality psychology as a methodological and ethical transition: from moralized character classification toward evidence-based, multidimensional, culturally aware, and developmentally informed personality science.

## Research focus

The central question is:

> How did personality psychology move from moralized character typologies and clinical portraits toward a modern science of traits, measurement, stability, person-situation interaction, culture, and narrative identity?

The scaffold examines:

- characterology-to-trait transitions
- typology versus dimensional scoring
- item-level trait structure
- reliability and measurement error
- exploratory dimensionality inspection
- three-, five-, and six-factor comparison
- rank-order stability across two time points
- person-situation interaction
- cultural and measurement-invariance cautions
- professional-use boundaries and responsible interpretation

## Structure

```text
data/        synthetic personality-history item data, SQL-ready scores, data dictionary, provenance notes
docs/        methods, reproducibility, professional-use boundary, responsible interpretation
python/      Python personality-history workflow
r/           R personality-history workflow
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
python3 python/analyze_personality_history.py
Rscript r/analyze_personality_history.R
sqlite3 outputs/personality_history.sqlite < sql/schema_and_queries.sql
```

## Professional Use Boundary

This repository may be used for professional education, research prototyping, psychometric demonstration, reproducible workflow development, consulting support, organizational learning, coaching reflection, and careful discussion of personality-history methods.

It is appropriate for demonstrating the movement from types to dimensions, reliability, latent structure, stability, person-situation modeling, measurement-invariance cautions, and historical reflection on assessment power.

This repository is not a standalone assessment or decision system for consequential decisions about individuals. It should not be used for hiring, promotion, termination, clinical diagnosis, educational placement, legal evaluation, insurance decisions, surveillance, relationship matching, moral labeling, or individual prediction unless substantially redesigned, validated for that specific purpose, reviewed by qualified professionals, and governed by appropriate ethical, legal, privacy, consent, fairness, measurement-invariance, cultural-validity, and psychometric safeguards.

The intended professional use is analytic, educational, methodological, historical, and reflective — not classificatory, predictive, surveillance-based, moralizing, or gatekeeping.

## Companion article

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/the-history-of-personality-psychology-from-characterology-to-personality-science>
