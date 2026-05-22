#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_traits_character_morality.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_traits_character.py","r/analyze_traits_character.R","sql/schema_and_queries.sql",
 "julia/analyze_traits_character.jl","go/traits_character_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/traits_character_summary.c","cpp/traits_character_summary.cpp","fortran/traits_character_summary.f90",
 "notebooks/traits_character_notebook.ipynb"
]
required_cols = {
 "participant_id","evaluation_context","honesty_humility","conscientiousness","agreeableness","emotional_stability","openness",
 "moral_identity","practical_judgment","institutional_accountability","power_pressure","social_desirability_pressure",
 "ethical_behavior","integrity_rating","trustworthiness_rating","descriptive_trait_reliability","moral_character_index",
 "judgment_context_index","trait_character_gap"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_traits_character_morality.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 100: errors.append(f"Expected at least 100 rows, found {len(rows)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
