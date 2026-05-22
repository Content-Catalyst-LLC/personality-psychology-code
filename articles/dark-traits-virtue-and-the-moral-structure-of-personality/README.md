# Dark Traits, Virtue, and the Moral Structure of Personality

This directory provides reproducible research scaffolding for the article **“Dark Traits, Virtue, and the Moral Structure of Personality.”** It supports a dimensional moral-personality workflow focused on dark traits, virtue-relevant tendencies, moral identity, practical judgment, institutional accountability, unethical behavior, prosocial restraint, and harm indicators.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how Machiavellianism, narcissism, psychopathy, sadism, Honesty-Humility, conscientious reliability, fairness, compassion, moral identity, practical judgment, and institutional incentives can be modeled without reducing moral character to a single score.

## Research focus

The central question is:

> How can personality psychology model morally consequential traits without collapsing moral character into either dark-trait burden or virtue-strength scores alone?

The scaffold examines:

- Dark Triad and Dark Tetrad constructs
- a shared dark-trait burden index
- Honesty-Humility as a morally central personality dimension
- virtue-relevant tendencies as positive constructs, not merely low darkness
- moral identity and practical judgment as additional layers
- institutional accountability as a moderator of harm
- profile groups combining darkness and virtue-relevant tendencies
- dominant dark-trait profiles and moral-outcome summaries

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
python3 python/analyze_dark_traits_virtue.py
Rscript r/analyze_dark_traits_virtue.R
sqlite3 outputs/dark_traits_virtue.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository provides a transparent research scaffold for studying the moral structure of personality. Its purpose is to support reproducible method development: synthetic data generation, dimensional construct modeling, dark-trait and virtue-relevant profile analysis, institutional-accountability modeling, cross-language workflow validation, and careful documentation of how dark traits, virtue-relevant tendencies, motive, judgment, and social incentives can be represented analytically.

The synthetic dataset is included so the workflow can be inspected, replicated, and extended without relying on sensitive human-subject data. Its patterns are constructed examples for testing model architecture, not empirical claims about actual people, communities, workplaces, leaders, institutions, or moral character.

The interpretive standard is disciplined and formulation-oriented. Dark traits should be understood through stable tendencies toward manipulation, entitlement, callousness, deception, exploitation, or cruelty. Virtue-relevant traits should be understood as positive moral tendencies that require motive, judgment, and practice. Low darkness does not automatically equal virtue, and measured virtue-relevant tendencies do not exhaust moral character.

This scaffold is best used to clarify concepts, test reproducible workflows, and support careful research design. It preserves the distinction between methodological modeling and moral judgment while treating personality as ethically consequential in relationships, institutions, power, trust, and harm.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/dark-traits-virtue-and-the-moral-structure-of-personality>
