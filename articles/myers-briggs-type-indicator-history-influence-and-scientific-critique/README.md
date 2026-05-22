# Myers-Briggs Type Indicator: History, Influence, and Scientific Critique

This directory provides reproducible research scaffolding for the article **“The Myers-Briggs Type Indicator: History, Influence, and Scientific Critique.”** It supports a dimensional-versus-typological workflow focused on continuous preference dimensions, dichotomous cutpoints, four-letter type construction, threshold instability, boundary cases, within-type variation, information loss, retest volatility, and model comparison.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show why MBTI-style type labels can feel meaningful and socially useful while still losing psychometric information relative to dimensional trait continua.

## Research focus

The central question is:

> What happens when continuous personality variation is compressed into memorable typological categories?

The scaffold examines:

- four continuous latent preference dimensions
- observed scores with measurement fluctuation
- MBTI-style dichotomous thresholds
- four-letter type-code construction
- boundary proximity and threshold fragility
- retest type stability
- type-frequency summaries
- within-type variation
- continuous-vs-categorical model comparison
- information loss after dichotomization
- appropriate interpretive boundaries for typological frameworks

## Structure

```text
data/        synthetic typology-vs-trait dataset, data dictionary, provenance notes
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
python3 python/analyze_mbti_typology_vs_traits.py
Rscript r/analyze_mbti_typology_vs_traits.R
sqlite3 outputs/mbti_typology_vs_traits.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository supports transparent, reproducible research scaffolding for examining MBTI-style typology, dimensional personality measurement, and the scientific consequences of dichotomizing continuous variation. It is designed for method development, synthetic-data testing, threshold analysis, type-frequency summaries, boundary-case identification, model comparison, and cross-language workflow validation.

The dataset is synthetic so the workflow can be inspected, replicated, and extended without using sensitive human-subject data. The patterns are constructed examples for testing measurement architecture, not claims about real MBTI users, employees, students, clients, teams, organizations, schools, communities, cultures, or institutions.

The interpretive standard is proportional. A type code can be useful as a conversational or reflective shorthand, but it should not be treated as a full account of a person. Continuous scores often preserve information that dichotomous labels discard. Boundary cases require particular caution, because small score differences or measurement fluctuation can change a categorical assignment without indicating a meaningful change in personality.

## Professional Use Boundary

This repository may be used for professional education, research prototyping, methodological demonstration, reproducible workflow development, organizational learning, consulting support, workshop materials, and critical analysis of personality typologies and dimensional measurement.

It is appropriate for demonstrating how typological systems compress continuous variation, how threshold effects create boundary cases, how retest instability can occur near cutpoints, and how dimensional models can preserve information that categorical labels may discard.

This repository should not be used as a standalone assessment system for making consequential decisions about individuals. It should not be used for hiring, promotion, termination, clinical assessment, diagnosis, educational placement, legal evaluation, relationship matching, or individual prediction unless it is substantially redesigned, validated for that specific purpose, reviewed by qualified professionals, and governed by appropriate ethical, legal, privacy, and psychometric safeguards.

The intended professional use is analytic, educational, methodological, and reflective — not classificatory or gatekeeping.
## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/myers-briggs-type-indicator-history-influence-and-scientific-critique>
