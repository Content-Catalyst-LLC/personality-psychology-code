#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_change_intervention.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_personality_change.py","r/analyze_personality_change.R","sql/schema_and_queries.sql",
 "julia/analyze_personality_change.jl","go/personality_change_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/personality_change_summary.c","cpp/personality_change_summary.cpp","fortran/personality_change_summary.f90",
 "notebooks/personality_change_notebook.ipynb"
]
required_cols = {
 "person_id","wave","wave_numeric","intervention_group","age","neuroticism","extraversion","conscientiousness",
 "openness","agreeableness","role_investment","state_practice_frequency","perceived_support"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_personality_change_intervention.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 300: errors.append(f"Expected at least 300 longitudinal rows, found {len(rows)}")
        people = {row.get("person_id") for row in rows}
        waves = {row.get("wave_numeric") for row in rows}
        groups = {row.get("intervention_group") for row in rows}
        if len(people) < 70: errors.append(f"Expected at least 70 synthetic people, found {len(people)}")
        if len(waves) < 4: errors.append(f"Expected at least 4 waves, found {len(waves)}")
        if not {"intervention", "comparison"}.issubset(groups): errors.append(f"Expected intervention and comparison groups, found {sorted(groups)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
