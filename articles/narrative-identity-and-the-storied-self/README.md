# Narrative Identity and the Storied Self

This directory provides reproducible research scaffolding for the article **“Narrative Identity and the Storied Self.”** It supports a dimensional workflow focused on redemption, contamination, coherence, agency, communion, meaning-making, narrative flexibility, defensive rigidity, self-continuity, wellbeing, and narrative-profile patterns.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how life stories can be studied as structured dimensions of personality without reducing persons to literary impressions, trait summaries, or simplistic growth scores.

## Research focus

The central question is:

> How can personality psychology study life stories as patterned, consequential, and socially situated structures of selfhood?

The scaffold examines:

- redemption and contamination themes
- narrative coherence
- agency and communion
- meaning-making
- narrative flexibility
- defensive rigidity
- self-continuity
- wellbeing
- narrative growth orientation
- narrative burden
- narrative integration
- redemptive agency balance
- narrative context summaries
- narrative profile summaries
- constrained narrative patterns such as high coherence with high defensiveness

## Structure

```text
data/        synthetic narrative-identity dataset, data dictionary, provenance notes
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
python3 python/analyze_narrative_identity.py
Rscript r/analyze_narrative_identity.R
sqlite3 outputs/narrative_identity.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository provides a transparent research scaffold for studying narrative identity and the storied self as multidimensional features of personality organization. Its purpose is to support reproducible method development: synthetic data generation, narrative-theme analysis, self-continuity modeling, profile summaries, cross-language workflow validation, and careful documentation of how redemption, contamination, coherence, agency, communion, meaning-making, narrative flexibility, defensive rigidity, and wellbeing can be represented analytically.

The synthetic dataset is included so the workflow can be inspected, replicated, and extended without relying on sensitive life-history, interview, clinical, educational, legal, workplace, or community data. Its patterns are constructed examples for testing model architecture, not empirical claims about actual people, survivors, patients, families, communities, cultures, institutions, or historical groups.

The interpretive standard is disciplined and contextual. A person’s life story cannot be reduced to a redemption score, contamination score, coherence index, agency code, or wellbeing outcome. Narrative identity is shaped by memory, culture, power, trauma, social recognition, institutional silencing, family history, public language, and available futures. Fragmented or non-redemptive stories may contain truth that a more polished story would erase.

This scaffold is best used to clarify concepts, test reproducible workflows, and support careful research design. It preserves the distinction between methodological modeling and evaluation of persons while treating life stories as meaningful, situated, revisable, and ethically weighty forms of self-understanding.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/narrative-identity-and-the-storied-self>
