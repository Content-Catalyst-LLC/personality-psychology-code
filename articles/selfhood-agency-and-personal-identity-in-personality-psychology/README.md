# Selfhood, Agency, and Personal Identity in Personality Psychology

This directory provides reproducible research scaffolding for the article **“Selfhood, Agency, and Personal Identity in Personality Psychology.”** It supports a dimensional workflow focused on temporal self-continuity, agency, action ownership, intentional clarity, self-efficacy, social recognition, external constraint, value–commitment alignment, identity integration, wellbeing, and personal identity patterns.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how selfhood and agency can be represented analytically without reducing persons to identity scores, trait inventories, or simple self-esteem measures.

## Research focus

The central question is:

> How can personality psychology study persons as agentive selves organized through continuity, authorship, recognition, commitment, and action across time?

The scaffold examines:

- past-present self-continuity
- present-future self-continuity
- temporal self-continuity
- intentional clarity
- action ownership
- self-efficacy
- external constraint
- social recognition
- value–commitment gap
- identity alignment
- agency index
- situated agency index
- identity integration
- wellbeing
- identity profile groups
- disjunction patterns such as high constraint with low agency

## Structure

```text
data/        synthetic selfhood-agency-identity dataset, data dictionary, provenance notes
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
python3 python/analyze_selfhood_agency_identity.py
Rscript r/analyze_selfhood_agency_identity.R
sqlite3 outputs/selfhood_agency_identity.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository provides a transparent research scaffold for studying selfhood, agency, and personal identity as multidimensional features of personality organization. Its purpose is to support reproducible method development: synthetic data generation, temporal self-continuity analysis, agency and recognition modeling, value–commitment alignment analysis, identity-profile summaries, cross-language workflow validation, and careful documentation of how persons can be studied as selves who experience ownership, continuity, recognition, and authorship across time.

The synthetic dataset is included so the workflow can be inspected, replicated, and extended without relying on sensitive human-subject data. Its patterns are constructed examples for testing model architecture, not empirical claims about actual people, patients, students, workers, families, communities, cultures, legal subjects, or institutions.

The interpretive standard is disciplined and contextual. A person’s selfhood cannot be reduced to a continuity score, agency index, identity-integration score, or wellbeing measure. Agency is situated in body, health, disability, social class, race, gender, law, family, labor conditions, violence, care responsibilities, institutions, recognition, and available support. Low agency or disrupted continuity may reflect real constraint, coercion, exclusion, trauma, displacement, moral injury, illness, or social erasure.

This scaffold is best used to clarify concepts, test reproducible workflows, and support careful research design. It preserves the distinction between methodological modeling and evaluation of persons while treating selfhood as embodied, relational, historical, socially recognized, and still open to repair.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/selfhood-agency-and-personal-identity-in-personality-psychology>
