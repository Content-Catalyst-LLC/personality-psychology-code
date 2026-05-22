# Personality, Relationships, and Social Functioning

This directory provides reproducible research scaffolding for the article **“Personality, Relationships, and Social Functioning.”** It supports a relational-personality workflow focused on personality traits, relationship satisfaction, friendship, attachment security, social functioning, loneliness, conflict, reciprocity, perceived support, reputation, and the social conditions under which personality becomes lived reality.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how personality, empathy, self-regulation, attachment security, social support, and context can be modeled without reducing relationships to individual traits alone.

## Research focus

The article asks a central question:

> How do enduring personality differences become socially consequential through intimacy, friendship, conflict, trust, reciprocity, support, exclusion, and broader social functioning?

This directory operationalizes that question through synthetic examples that examine:

- Big Five trait associations with relationship outcomes
- empathy and self-regulation as relational capacities
- attachment security and perceived support
- relationship satisfaction and broader social functioning
- loneliness, conflict, and social breakdown
- reciprocity quality and reputation trust
- social context and relationship-domain differences
- the difference between individual traits and dyadic / structural conditions

## Directory structure

```text
personality-relationships-and-social-functioning/
├── README.md
├── UPGRADE_MANIFEST.md
├── Makefile
├── config/
│   └── analysis_config.yml
├── data/
│   ├── synthetic_personality_relationships_social_functioning.csv
│   ├── data_dictionary.md
│   └── provenance.md
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── responsible-research-use.md
├── python/
│   └── analyze_personality_relationships.py
├── r/
│   └── analyze_personality_relationships.R
├── sql/
│   └── schema_and_queries.sql
├── julia/
│   └── analyze_personality_relationships.jl
├── go/
│   └── relationships_summary.go
├── rust/
│   ├── Cargo.toml
│   └── src/main.rs
├── c/
│   └── relationships_summary.c
├── cpp/
│   └── relationships_summary.cpp
├── fortran/
│   └── relationships_summary.f90
├── notebooks/
│   └── personality_relationships_notebook.ipynb
├── validation/
│   ├── validate_repository.py
│   └── run_validation.sh
└── outputs/
    └── .gitkeep
```

## Data

The included dataset is synthetic. It is structured to support reproducible demonstrations of relational-personality analysis while avoiding claims about real persons, partners, families, friendships, communities, or actual social outcomes.

The data include:

- `social_context`
- `relationship_domain`
- Big Five trait scores
- `empathy`
- `self_regulation`
- `attachment_security`
- `perceived_support`
- `relationship_satisfaction`
- `social_functioning`
- `loneliness`
- `conflict_frequency`
- `reciprocity_quality`
- `reputation_trust`

## Core concepts

### Relationships are not one-person outcomes

Relationship quality depends on actor traits, partner traits, dyadic fit, social context, stress, support, culture, and repair capacity.

### Social functioning is broader than popularity

Healthy social functioning includes reciprocity, trust, conflict repair, perceived support, belonging, reliability, and the ability to participate in social life without chronic breakdown.

### Traits become relational through behavior

Traits become socially meaningful when they shape listening, repair, escalation, withdrawal, care, reliability, reciprocity, and reputation.

### Context changes interpretation

Loneliness, conflict, and social functioning can reflect both personality and social conditions, including exclusion, disability, poverty, discrimination, caregiving burden, grief, or lack of safe community.

## Quick start

Run the validation script:

```bash
bash validation/run_validation.sh
```

Run the Python workflow:

```bash
python3 python/analyze_personality_relationships.py
```

Run the R workflow:

```bash
Rscript r/analyze_personality_relationships.R
```

Run SQL examples with SQLite:

```bash
sqlite3 outputs/personality_relationships.sqlite < sql/schema_and_queries.sql
```

Run the Makefile workflow:

```bash
make validate
make python
```

## Outputs

Generated outputs are written to `outputs/`, including:

- social-context summaries
- relationship-domain summaries
- trait correlation matrices
- relational stability and conflict-risk indices
- relationship, social functioning, loneliness, and conflict model outputs
- validation reports

## Responsible Research Use

This repository is designed for reproducible, research-oriented analysis of personality, relationships, and social functioning. Its purpose is to support careful thinking about traits, empathy, self-regulation, attachment security, support, loneliness, conflict, reciprocity, reputation, and social context.

The examples use synthetic data so the workflows can be inspected, adapted, and extended without relying on private relationship records or making claims about actual individuals, couples, families, friendship networks, or communities. The emphasis is on transparent methods, reproducible code, and disciplined interpretation.

Relational-personality analysis should be handled with particular care. Apparent differences in relationship satisfaction, social functioning, loneliness, or conflict may reflect partner dynamics, family systems, trauma history, disability, discrimination, poverty, caregiving burden, cultural norms, exclusion, social support, measurement design, or current stress rather than stable traits alone.

The strongest use of this scaffold is developmental and relational: examining how personality and social worlds interact, distinguishing relationship quality from broad popularity, and treating social difficulty with dignity rather than reducing people to labels.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/personality-relationships-and-social-functioning>
