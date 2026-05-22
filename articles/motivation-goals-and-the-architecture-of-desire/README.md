# Motivation, Goals, and the Architecture of Desire

This directory provides reproducible research scaffolding for the article **“Motivation, Goals, and the Architecture of Desire.”** It supports a dimensional workflow focused on goal priorities, psychological need support, goal ownership, goal conflict, motivational quality, persistence, adaptive disengagement, wellbeing, and life-direction coherence.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how personality can be studied not only as trait structure, but as directed life organization: what people pursue, how goals are ordered, how conflict changes regulation, and how environments support or deform the quality of striving.

## Research focus

The central question is:

> How can personality psychology study desire as a structured system of needs, motives, goals, ownership, conflict, self-regulation, and social context?

The scaffold examines:

- autonomy, achievement, belonging, security, meaning, and status goals
- psychological need support: autonomy, competence, and relatedness
- goal ownership and motivational quality
- approach orientation and avoidance/security orientation
- status orientation and meaning orientation
- goal conflict
- conscientiousness and persistence
- adaptive disengagement
- wellbeing
- life-direction coherence
- motivational profile groups
- vulnerable patterns such as high conflict with low ownership and high status with low meaning

## Structure

```text
data/        synthetic motivation-and-goals dataset, data dictionary, provenance notes
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
python3 python/analyze_motivation_goals_desire.py
Rscript r/analyze_motivation_goals_desire.R
sqlite3 outputs/motivation_goals_desire.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository supports transparent, reproducible research scaffolding for studying motivation, goals, and the architecture of desire. It is designed for method development, synthetic-data testing, goal-system analysis, self-determination modeling, self-regulation summaries, motivational profile construction, and cross-language workflow validation.

The dataset is synthetic so the workflow can be inspected, replicated, and extended without relying on sensitive human-subject data. The patterns are constructed examples for testing model architecture, not empirical claims about real people, patients, students, workers, families, communities, institutions, workplaces, schools, cultures, religious traditions, or political groups.

The interpretive standard is contextual. Motivation is shaped by family, school, work, class, culture, religion, institutions, trauma, opportunity, coercion, recognition, and available futures. A goal profile or persistence score is an analytic signal, not a judgment about a person’s worth. Persistence can reflect courage or compulsion. Disengagement can reflect avoidance or wisdom. Security goals may reflect real exposure to danger. Status goals may reflect vanity, but also dignity, survival, or escape from exclusion.

Use this scaffold to clarify concepts, test reproducible workflows, and support careful research design. The repository’s outputs should not be used to classify individuals, rank moral worth, screen workers or students, make clinical judgments, or infer the quality of a life from synthetic model results.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/motivation-goals-and-the-architecture-of-desire>
