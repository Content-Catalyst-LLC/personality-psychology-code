# Reproducibility Notes

## Inputs

- `data/synthetic_personality_creativity.csv`
- `data/data_dictionary.md`
- `data/provenance.md`

## Outputs

Generated files should be written to:

- `outputs/tables/`
- `outputs/figures/`

## Recommended execution order

```bash
python3 python/analyze_personality_creativity.py
Rscript r/analyze_personality_creativity.R
sqlite3 outputs/tables/personality_creativity.sqlite < sql/schema_and_queries.sql
bash validation/run_validation.sh
```

## Dependency philosophy

The examples use light dependencies and standard formats so they can be inspected, ported, and adapted easily.
