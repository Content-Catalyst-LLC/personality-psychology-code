# Upgrade Manifest

## Article directory

`articles/personality-culture-and-the-problem-of-universality`

## Upgrade purpose

This upgrade turns the article companion folder into a professional research scaffold for cross-cultural personality psychology. It preserves the existing multi-language layout while adding stronger documentation, reproducible synthetic data, validation tooling, and cross-language examples.

## Added or upgraded components

- Professional README
- Data dictionary
- Provenance notes
- Methods documentation
- Reproducibility documentation
- Responsible-use documentation
- Synthetic cross-cultural personality dataset
- Python workflow
- R workflow
- SQL schema and queries
- Julia workflow
- Go matrix-similarity example
- Rust matrix-similarity example
- C summary example
- C++ summary example
- Fortran summary example
- Jupyter notebook scaffold
- Validation scripts
- Makefile commands

## Research-grade goals

This directory is intended to demonstrate:

1. Clear distinction between broad trait recurrence and strict universality.
2. Transparent handling of synthetic data.
3. Reproducible multi-language workflow design.
4. Caution about measurement invariance and cross-cultural interpretation.
5. Avoidance of diagnostic, population-ranking, or screening uses.
6. Professional documentation suitable for a public knowledge repository.

## Validation

Run:

```bash
bash validation/run_validation.sh
```

The validation script checks for required folders, expected files, readable data, expected columns, and basic row counts.
