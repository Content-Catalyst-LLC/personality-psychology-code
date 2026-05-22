# Personality and Political Behavior

This directory provides reproducible research scaffolding for the article **“Personality and Political Behavior.”** It supports a political-psychology workflow focused on personality traits, ideology, participation, civic engagement, threat perception, political efficacy, identity attachment, institutional trust, leadership preference, and affective polarization.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how personality, political context, identity, institutions, media exposure, and civic opportunity can be modeled without reducing politics to traits or treating citizens as interchangeable processors of information.

## Research focus

The article asks a central question:

> How do enduring personality differences shape political attitudes, participation, identity, threat perception, leadership preference, and civic behavior under specific institutional and historical conditions?

This directory operationalizes that question through synthetic examples that examine:

- Big Five trait associations with ideology and participation
- political efficacy and civic opportunity as participation pathways
- identity-threat dynamics and affective polarization
- openness, conscientiousness, and contextual ideology models
- leadership-authority preference and threat sensitivity
- institutional trust as an outcome of traits and political context
- the difference between personality effects and political-context effects

## Directory structure

```text
personality-and-political-behavior/
├── README.md
├── UPGRADE_MANIFEST.md
├── Makefile
├── config/
│   └── analysis_config.yml
├── data/
│   ├── synthetic_personality_political_behavior.csv
│   ├── data_dictionary.md
│   └── provenance.md
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── responsible-research-use.md
├── python/
│   └── analyze_personality_political_behavior.py
├── r/
│   └── analyze_personality_political_behavior.R
├── sql/
│   └── schema_and_queries.sql
├── julia/
│   └── analyze_personality_political_behavior.jl
├── go/
│   └── political_summary.go
├── rust/
│   ├── Cargo.toml
│   └── src/main.rs
├── c/
│   └── political_summary.c
├── cpp/
│   └── political_summary.cpp
├── fortran/
│   └── political_summary.f90
├── notebooks/
│   └── personality_political_behavior_notebook.ipynb
├── validation/
│   ├── validate_repository.py
│   └── run_validation.sh
└── outputs/
    └── .gitkeep
```

## Data

The included dataset is synthetic. It is structured to support reproducible demonstrations of political-behavior analysis while avoiding claims about real voters, real citizens, real countries, real parties, or actual political outcomes.

The data include:

- `country_context`
- `political_system_type`
- Big Five trait scores
- `political_interest`
- `political_efficacy`
- `group_identity_strength`
- `perceived_threat`
- `media_exposure`
- `civic_opportunity`
- `ideology_score`
- `political_participation`
- `affective_polarization`
- `trust_in_institutions`
- `leadership_authority_preference`

## Core concepts

### Personality and ideology

Traits may shape ideological style, issue interpretation, and political concern, but they do not mechanically produce one fixed ideology.

### Personality and participation

Participation depends on motivation, efficacy, opportunity, social energy, civic resources, and institutional conditions.

### Identity and threat

Group identity and perceived threat can interact with traits to shape affective polarization and public conflict.

### Context-sensitive politics

Trait-politics relations vary by issue domain, country, party system, political context, and historical meaning.

## Quick start

Run the validation script:

```bash
bash validation/run_validation.sh
```

Run the Python workflow:

```bash
python3 python/analyze_personality_political_behavior.py
```

Run the R workflow:

```bash
Rscript r/analyze_personality_political_behavior.R
```

Run SQL examples with SQLite:

```bash
sqlite3 outputs/personality_political_behavior.sqlite < sql/schema_and_queries.sql
```

Run the Makefile workflow:

```bash
make validate
make python
```

## Outputs

Generated outputs are written to `outputs/`, including:

- political context summaries
- trait correlation matrices
- participation and ideology model outputs
- identity-threat and affective polarization metrics
- institutional trust summaries
- validation reports

## Responsible Research Use

This repository is designed for reproducible, research-oriented analysis of personality and political behavior. Its purpose is to support careful thinking about traits, ideology, participation, identity, threat perception, institutional trust, and the limits of universal trait-politics mappings.

The examples use synthetic data so the workflows can be inspected, adapted, and extended without relying on private survey data or making claims about actual voters, groups, parties, or countries. The emphasis is on transparent methods, reproducible code, and disciplined interpretation.

Political personality analysis should be handled with particular care. Apparent differences in political behavior may reflect institutions, media systems, class position, race, religion, education, geography, historical memory, group identity, civic opportunity, or measurement design rather than stable individual traits alone.

The strongest use of this scaffold is comparative and civic: examining how personality and political context interact, clarifying the pathways through which citizens participate or withdraw, and avoiding simplistic explanations that pathologize disagreement or reduce political conflict to personality alone.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/personality-and-political-behavior>
