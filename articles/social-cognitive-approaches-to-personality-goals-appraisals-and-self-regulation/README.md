# Social-Cognitive Approaches to Personality: Goals, Appraisals, and Self-Regulation

This directory provides reproducible research scaffolding for the article **“Social-Cognitive Approaches to Personality: Goals, Appraisals, and Self-Regulation.”** It supports a repeated-measures workflow focused on how personality is enacted through goals, appraisals, expectancies, self-efficacy, self-regulation, perceived support, situation types, and behavior over time.

The repository is designed as a serious companion to the article. It links conceptual analysis to reproducible synthetic-data examples that show how social-cognitive personality processes can be modeled without reducing persons to trait labels or process scores.

## Research focus

The central question is:

> How can personality psychology model enduring individuality as a dynamic system of goals, appraisals, expectancies, and self-regulation across situations?

The scaffold examines:

- goal activation
- threat appraisal and challenge appraisal
- self-efficacy
- self-regulation
- emotional arousal
- perceived support
- situation types
- prosocial behavior
- avoidance behavior
- task persistence
- CAPS-style if–then summaries
- person-level and situation-level process summaries
- reciprocal person-environment process logic

## Structure

```text
data/        synthetic repeated-measures dataset, data dictionary, provenance notes
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
python3 python/analyze_social_cognitive_personality.py
Rscript r/analyze_social_cognitive_personality.R
sqlite3 outputs/social_cognitive_personality.sqlite < sql/schema_and_queries.sql
```

## Responsible Research Use

This repository provides a transparent research scaffold for studying social-cognitive personality processes. Its purpose is to support reproducible method development: synthetic repeated-measures data generation, person-situation process modeling, if–then pattern summaries, cross-language workflow validation, and careful documentation of how goals, appraisals, expectancies, self-regulation, support, and behavior can be represented analytically.

The synthetic dataset is included so the workflow can be inspected, replicated, and extended without relying on sensitive human-subject data. Its patterns are constructed examples for testing model architecture, not empirical claims about actual people, students, patients, workers, classrooms, families, organizations, or communities.

The interpretive standard is disciplined and formulation-oriented. Goals, appraisals, expectancies, and self-regulation are powerful constructs, but they should not be used to blame people for learned vigilance, constrained agency, trauma-shaped expectations, exclusion, disability, poverty, institutional harm, or limited opportunity. Self-efficacy and regulation matter, but they are always situated within developmental, cultural, relational, and structural conditions.

This scaffold is best used to clarify concepts, test reproducible workflows, and support careful research design. It preserves the distinction between methodological modeling and assessment of persons while treating personality as a dynamic person-in-context system.

## Companion article

GitHub directory:

<https://github.com/Content-Catalyst-LLC/personality-psychology-code/tree/main/articles/social-cognitive-approaches-to-personality-goals-appraisals-and-self-regulation>
