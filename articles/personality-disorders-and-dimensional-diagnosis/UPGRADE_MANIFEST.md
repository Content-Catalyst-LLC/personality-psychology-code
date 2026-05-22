# Upgrade Manifest

## Article directory

`articles/personality-disorders-and-dimensional-diagnosis`

## Upgrade purpose

This upgrade turns the article companion folder into a professional research scaffold for studying personality disorders and dimensional diagnosis. It preserves the existing multi-language layout while adding stronger documentation, reproducible synthetic data, validation tooling, and cross-language examples.

## Added or upgraded components

- Professional README
- Data dictionary
- Provenance notes
- Methods documentation
- Reproducibility documentation
- Responsible Research Use documentation
- Synthetic dimensional personality-disorder dataset
- Python workflow
- R workflow
- SQL schema and queries
- Julia workflow
- Go summary example
- Rust summary example
- C summary example
- C++ summary example
- Fortran summary example
- Jupyter notebook scaffold
- Validation scripts
- Makefile commands

## Research-grade goals

This directory is intended to demonstrate:

1. Clear distinction between diagnostic severity, maladaptive trait domains, self-functioning impairment, interpersonal-functioning impairment, risk, and treatment engagement.
2. Transparent handling of synthetic data.
3. Reproducible multi-language workflow design.
4. Careful interpretation of DSM-5 AMPD-style and ICD-11-style dimensional concepts.
5. Avoidance of automated diagnosis, clinical decision-making, risk scoring, social ranking, or personality reductionism.
6. Professional documentation suitable for a public knowledge repository.

## Validation

Run:

```bash
bash validation/run_validation.sh
```

The validation script checks for required folders, expected files, readable data, expected columns, and basic row counts.
