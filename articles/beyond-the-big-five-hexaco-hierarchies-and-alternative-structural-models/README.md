# Beyond the Big Five: HEXACO, Hierarchies, and Alternative Structural Models

This directory provides reproducible research scaffolding for the article **“Beyond the Big Five: HEXACO, Hierarchies, and Alternative Structural Models.”** It supports a professional psychometric workflow focused on five-factor and six-factor comparison, HEXACO-style expansion, Honesty-Humility, hierarchical trait scoring, facet-level interpretation, bandwidth-fidelity tradeoffs, and structural model comparison.

The scaffold treats alternative personality structures as comparative maps rather than slogans. The Big Five provides a powerful high-bandwidth map. HEXACO makes Honesty-Humility and moral/exploitative interpersonal content more visible. Hierarchies show how domains, aspects, facets, and items relate across levels. Circumplex and network approaches show that structure can also be geometric or relational.

## Research focus

The central question is:

> When does personality science need a model beyond the Big Five, and how should alternative structures be compared responsibly?

The scaffold examines:

- five-factor and six-factor structural comparison
- HEXACO-style Honesty-Humility content
- Big Five-to-HEXACO repartitioning logic
- item-level personality structure
- broad domains and narrower facets
- hierarchical domain/facet scoring
- domain-versus-expanded-model prediction
- integrity-related and interpersonal outcomes
- bandwidth-fidelity tradeoffs
- structural-model comparison limits
- professional-use boundaries and responsible interpretation

## Structure

```text
data/        synthetic alternative-structure item data, SQL-ready scores, data dictionary, provenance notes
docs/        methods, reproducibility, professional-use boundary, responsible interpretation
python/      Python structural-comparison workflow
r/           R structural-comparison workflow
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
python3 python/analyze_alternative_structures.py
Rscript r/analyze_alternative_structures.R
sqlite3 outputs/alternative_structures.sqlite < sql/schema_and_queries.sql
```

## Professional Use Boundary

This repository may be used for professional education, research prototyping, psychometric demonstration, reproducible workflow development, consulting support, organizational learning, coaching reflection, and critical comparison of personality-structure models.

It is appropriate for demonstrating five-versus-six-factor comparison, HEXACO-style Honesty-Humility modeling, broad-versus-narrow prediction, hierarchical scoring, factor-score workflow design, bandwidth-fidelity tradeoffs, and the difference between structural description and consequential individual decision-making.

This repository is not a standalone assessment or decision system for consequential decisions about individuals. It should not be used for hiring, promotion, termination, clinical diagnosis, educational placement, legal evaluation, insurance decisions, surveillance, relationship matching, moral labeling, or individual prediction unless substantially redesigned, validated for that specific purpose, reviewed by qualified professionals, and governed by appropriate ethical, legal, privacy, consent, fairness, measurement-invariance, and psychometric safeguards.

The intended professional use is analytic, educational, methodological, and reflective — not classificatory, predictive, surveillance-based, moralizing, or gatekeeping.

## Companion article

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/beyond-the-big-five-hexaco-hierarchies-and-alternative-structural-models>
