#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_dynamics_data.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_personality_dynamics.py","r/analyze_personality_dynamics.R","sql/schema_and_queries.sql",
 "julia/analyze_personality_dynamics.jl","go/dynamics_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/dynamics_summary.c","cpp/dynamics_summary.cpp","fortran/dynamics_summary.f90",
 "notebooks/personality_dynamics_notebook.ipynb"
]
required_cols = {
 "person_id","assessment_context","occasion","trait_extraversion","trait_conscientiousness","trait_neuroticism",
 "state_extraversion","state_conscientiousness","state_neuroticism","situation_valence","situation_sociality",
 "situation_demand","situation_evaluation","positive_affect","negative_affect","goal_pressure","autonomy_support",
 "state_inertia_marker","dynamic_signature_score"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_personality_dynamics_data.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 1200: errors.append(f"Expected at least 1200 repeated-measure rows, found {len(rows)}")
        persons = {row.get("person_id") for row in rows}
        if len(persons) < 80: errors.append(f"Expected at least 80 synthetic persons, found {len(persons)}")
        contexts = {row.get("assessment_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 assessment contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
