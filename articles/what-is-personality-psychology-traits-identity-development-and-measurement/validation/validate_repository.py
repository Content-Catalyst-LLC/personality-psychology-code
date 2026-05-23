#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_items.csv","data/synthetic_person_situation_observations.csv","data/synthetic_personality_summary_for_sql.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_personality_psychology.py","r/analyze_personality_psychology.R","sql/schema_and_queries.sql",
 "julia/analyze_personality_psychology.jl","go/personality_psychology_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/personality_psychology_summary.c","cpp/personality_psychology_summary.cpp","fortran/personality_psychology_summary.f90",
 "notebooks/personality_psychology_notebook.ipynb"
]
personality_cols = {
 "person_id", *[f"item{i}" for i in range(1,61)], *[f"c{i}" for i in range(1,7)], *[f"e{i}" for i in range(1,7)], *[f"n{i}" for i in range(1,7)],
 "conscientiousness_score","extraversion_score","neuroticism_score",
 "identity_coherence","life_satisfaction","social_functioning","developmental_integration",
 "measurement_reliability_index","identity_trait_alignment_index","person_situation_sensitivity_index","responsible_interpretation_index"
}
state_cols = {"person_id","occasion","situation_type","behavior_score","trait_score","situation_strength","trait_x_situation","observed_regulation","contextual_constraint"}
summary_cols = {"person_id","conscientiousness_score","extraversion_score","neuroticism_score","identity_coherence","life_satisfaction","social_functioning","developmental_integration","measurement_reliability_index","identity_trait_alignment_index","person_situation_sensitivity_index","responsible_interpretation_index","mean_behavior_score","mean_situation_strength","mean_observed_regulation","mean_contextual_constraint"}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]

def check_csv(path, required, min_rows):
    if not path.exists():
        return
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required - set(reader.fieldnames or [])
        if missing:
            errors.append(f"{path.name} missing columns: {sorted(missing)}")
        if len(rows) < min_rows:
            errors.append(f"{path.name} expected at least {min_rows} rows, found {len(rows)}")
        ids = [row.get("person_id") for row in rows if "person_id" in row]
        if path.name != "synthetic_person_situation_observations.csv" and len(set(ids)) != len(ids):
            errors.append(f"{path.name} person_id values should be unique")

check_csv(ROOT / "data" / "synthetic_personality_items.csv", personality_cols, 800)
check_csv(ROOT / "data" / "synthetic_person_situation_observations.csv", state_cols, 10000)
check_csv(ROOT / "data" / "synthetic_personality_summary_for_sql.csv", summary_cols, 800)

if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
