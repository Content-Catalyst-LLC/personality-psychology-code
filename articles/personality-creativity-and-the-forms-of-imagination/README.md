# Personality, Creativity, and the Forms of Imagination

This directory provides professional research scaffolding for the article **“Personality, Creativity, and the Forms of Imagination”** in the Personality Psychology knowledge series.

The project treats creativity as a multi-component outcome shaped by personality traits, domain knowledge, persistence, social support, domain context, and measurement choices. It is designed for reproducible demonstration, teaching, exploratory modeling, and transparent computational reasoning.

## Research purpose

This repository supports three linked questions:

1. How do openness, intellect, conscientiousness, persistence, and social support relate to divergent thinking?
2. How do the same factors relate to creative achievement and everyday creativity?
3. How does the interpretation change when creative outcomes are separated rather than collapsed into a single creativity score?

The structure deliberately separates:

- **Divergent thinking** as ideational generation.
- **Creative achievement** as realized and recognized output.
- **Everyday creativity** as adaptive imagination in ordinary life.
- **Domain context** as a factor that can modify trait-outcome relations.

## Directory structure

```text
personality-creativity-and-the-forms-of-imagination/
├── c/                         # C implementation of descriptive statistics
├── cpp/                       # C++ implementation of correlation-style summaries
├── data/                      # Synthetic data, dictionary, and provenance notes
├── docs/                      # Methods, reproducibility, and responsible-use notes
├── fortran/                   # Fortran numerical summary example
├── go/                        # Go CLI-style data summary utility
├── julia/                     # Julia modeling workflow
├── notebooks/                 # Jupyter notebook scaffold
├── outputs/
│   ├── figures/               # Generated plots
│   └── tables/                # Generated tables/model summaries
├── python/                    # Python analysis workflow
├── r/                         # R analysis workflow
├── rust/                      # Rust data validation and summary example
├── sql/                       # SQL schema and analytic queries
└── validation/                # Cross-language validation notes and run script
```

## Data

The included dataset is synthetic and intentionally small. It is designed to make the modeling logic inspectable rather than to estimate real population effects.

Primary file:

```text
data/synthetic_personality_creativity.csv
```

Core variables include:

- `openness`
- `intellect`
- `conscientiousness`
- `extraversion`
- `agreeableness`
- `neuroticism`
- `persistence`
- `social_support`
- `domain`
- `divergent_thinking`
- `creative_achievement`
- `everyday_creativity`

See:

```text
data/data_dictionary.md
data/provenance.md
```

## Suggested workflow

From this article directory:

```bash
cd articles/personality-creativity-and-the-forms-of-imagination
```

Run Python:

```bash
python3 python/analyze_personality_creativity.py
```

Run R:

```bash
Rscript r/analyze_personality_creativity.R
```

Run SQL with SQLite:

```bash
sqlite3 outputs/tables/personality_creativity.sqlite < sql/schema_and_queries.sql
```

Run Julia:

```bash
julia julia/analyze_personality_creativity.jl
```

Run validation summary:

```bash
bash validation/run_validation.sh
```

## Methods summary

The core statistical framing uses regression-style models that separate divergent thinking from creative achievement:

\[
C_i = \alpha + \beta_1 O_i + \beta_2 D_i + \beta_3 E_i + \beta_4 S_i + \varepsilon_i
\]

where \(C_i\) is a creative outcome, \(O_i\) is openness-related disposition, \(D_i\) is domain knowledge or domain context, \(E_i\) is execution/persistence capacity, and \(S_i\) is social support or opportunity.

The computational examples are intended to demonstrate:

- descriptive statistics;
- correlation matrices;
- trait-outcome modeling;
- domain-sensitive interpretation;
- transparent data documentation;
- reproducible cross-language scaffolding.

## Responsible use

This repository is for research demonstration, teaching, and reproducible workflow development. The examples should not be used for clinical diagnosis, psychological screening, hiring selection, workplace evaluation, educational tracking, or individual assessment.

The central interpretive rule is simple: personality traits describe probabilistic tendencies at group level. They should not be converted into deterministic labels about individual creative worth.

## Reproducibility

The repository favors simple, inspectable examples over hidden dependencies. The Python and R workflows write outputs into:

```text
outputs/tables/
outputs/figures/
```

The validation script checks that the expected data and workflow files exist.

## Citation note

When reusing or adapting this material, cite the associated article and repository path.
