# Self-Concept, Self-Esteem, and Self-Knowledge

This directory provides reproducible research scaffolding for the article **“Self-Concept, Self-Esteem, and Self-Knowledge.”** It supports a dimensional workflow focused on self-representation, self-evaluation, self–other agreement, self-knowledge accuracy, self-discrepancy, social recognition, external devaluation, wellbeing, and self-system profile patterns.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how self-concept, self-esteem, and self-knowledge can be modeled as distinct but interdependent layers of personality architecture.

## Research focus

The central question is:

> How can personality psychology study the self as a system of representation, evaluation, accuracy, discrepancy, social reflection, and cultural recognition?

The scaffold examines:

- self-concept positivity
- self-esteem
- self–other agreement
- self-knowledge accuracy
- actual–ideal discrepancy
- actual–ought discrepancy
- total self-discrepancy
- social recognition
- external devaluation
- wellbeing
- high self-esteem with low self-knowledge accuracy
- low self-esteem with high external devaluation
- self-system profiles combining esteem, accuracy, and discrepancy

## Structure

```text
data/        synthetic self-system dataset, data dictionary, provenance notes
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
python3 python/analyze_self_concept_self_esteem_self_knowledge.py
Rscript r/analyze_self_concept_self_esteem_self_knowledge.R
sqlite3 outputs/self_concept_self_esteem_self_knowledge.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository provides a transparent research scaffold for studying self-concept, self-esteem, and self-knowledge as distinct but interdependent layers of personality organization. Its purpose is to support reproducible method development: synthetic data generation, self–other agreement analysis, self-discrepancy modeling, self-knowledge accuracy summaries, self-esteem modeling, self-system profile summaries, cross-language workflow validation, and careful documentation of how selfhood can be represented analytically without reducing persons to self-ratings.

The synthetic dataset is included so the workflow can be inspected, replicated, and extended without relying on sensitive human-subject data. Its patterns are constructed examples for testing model architecture, not empirical claims about actual people, patients, students, workers, families, communities, schools, workplaces, cultures, institutions, or clinical populations.

The interpretive standard is disciplined and contextual. A person cannot be reduced to a self-esteem score, self-concept profile, self–other agreement coefficient, or discrepancy index. Selfhood is shaped by family, culture, disability, class, race, gender, religion, language, labor conditions, health, social recognition, and institutional treatment. Low self-esteem, self-discrepancy, or limited self-knowledge may reflect real constraint, trauma, misrecognition, exclusion, devaluation, depression, illness, or unavailable corrective feedback.

This scaffold is best used to clarify concepts, test reproducible workflows, and support careful research design. It preserves the distinction between methodological modeling and evaluation of persons while treating the self as representational, evaluative, epistemic, social, developmental, and open to repair.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/self-concept-self-esteem-and-self-knowledge>
