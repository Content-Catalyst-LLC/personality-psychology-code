# Trait Hierarchies, Facets, and the Architecture of Personality

This directory provides reproducible research scaffolding for the article **“Trait Hierarchies, Facets, and the Architecture of Personality.”** It supports a professional psychometric workflow focused on broad domains, aspects, facets, item-level structure, reliability, hierarchical measurement, bandwidth-fidelity tradeoffs, and domain-versus-facet prediction.

The scaffold treats trait hierarchies as a theory of scale. Broad domains support high-bandwidth summary. Facets support higher-fidelity interpretation. Item-level data preserve local psychological content. The goal is to show how personality structure can be modeled across levels without confusing one level for the whole person.

## Research focus

The central question is:

> How should personality psychology decide whether to describe, measure, and interpret traits at the level of domains, aspects, facets, nuances, or items?

The scaffold examines:

- broad domain scoring
- facet scoring within domains
- item-level structure
- reliability by level
- domain-versus-facet prediction
- bandwidth-fidelity tradeoffs
- hierarchical factor interpretation
- cultural and measurement-invariance cautions
- professional-use boundaries for hierarchical assessment
- responsible interpretation of granular personality scores

## Structure

```text
data/        synthetic hierarchical trait item dataset, data dictionary, provenance notes
docs/        methods, reproducibility, professional-use boundary, responsible interpretation
python/      Python psychometric workflow
r/           R psychometric workflow
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
python3 python/analyze_trait_hierarchies.py
Rscript r/analyze_trait_hierarchies.R
sqlite3 outputs/trait_hierarchies.sqlite < sql/schema_and_queries.sql
```

## Professional Use Boundary

This repository may be used for professional education, research prototyping, psychometric demonstration, reproducible workflow development, consulting support, organizational learning, coaching reflection, and critical analysis of hierarchical trait measurement.

It is appropriate for demonstrating item-to-facet aggregation, facet-to-domain aggregation, reliability by measurement level, broad-versus-narrow prediction, bandwidth-fidelity tradeoffs, and the difference between structural description and consequential individual decision-making.

This repository is not a standalone assessment or decision system for consequential decisions about individuals. It should not be used for hiring, promotion, termination, clinical diagnosis, educational placement, legal evaluation, insurance decisions, surveillance, relationship matching, or individual prediction unless substantially redesigned, validated for that specific purpose, reviewed by qualified professionals, and governed by appropriate ethical, legal, privacy, consent, fairness, measurement-invariance, and psychometric safeguards.

The intended professional use is analytic, educational, methodological, and reflective — not classificatory, predictive, surveillance-based, or gatekeeping.

## Companion article

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/trait-hierarchies-facets-and-the-architecture-of-personality>
