# Reproducibility

## Expected environment

The workflows are intentionally simple and use common tools.

Recommended:

- Python 3.10+
- R 4.2+
- SQLite 3
- Julia 1.9+
- Go 1.20+
- Rust 1.70+
- GCC / Clang
- gfortran

## Basic workflow

```bash
make validate
make python
make r
make sql
```

## Output policy

Generated files should be written to `outputs/`.

## Reproducibility principles

- Keep raw or synthetic input data in `data/`.
- Keep code in language-specific folders.
- Keep generated outputs out of source logic.
- Document assumptions in `docs/`.
- Validate expected files before analysis.
- Avoid hidden local paths or machine-specific dependencies.
