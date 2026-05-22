#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_dark_traits_virtue_personality.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_dark_traits_virtue.py","r/analyze_dark_traits_virtue.R","sql/schema_and_queries.sql",
 "julia/analyze_dark_traits_virtue.jl","go/dark_traits_virtue_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/dark_traits_virtue_summary.c","cpp/dark_traits_virtue_summary.cpp","fortran/dark_traits_virtue_summary.f90",
 "notebooks/dark_traits_virtue_notebook.ipynb"
]
required_cols = {
 "participant_id","institutional_context","machiavellianism","narcissism","psychopathy","sadism",
 "honesty_humility","conscientious_reliability","fairness_orientation","compassion_kindness",
 "moral_identity","practical_judgment","institutional_accountability","status_reward_pressure",
 "unethical_behavior","prosocial_restraint","harm_indicator","dark_trait_burden","virtue_relevant_tendency",
 "moral_integration_index","dark_accountability_risk"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_dark_traits_virtue_personality.csv"
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
