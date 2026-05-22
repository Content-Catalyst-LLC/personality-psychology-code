#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_person_situation_data.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_person_situation_debate.py","r/analyze_person_situation_debate.R","sql/schema_and_queries.sql",
 "julia/analyze_person_situation_debate.jl","go/person_situation_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/person_situation_summary.c","cpp/person_situation_summary.cpp","fortran/person_situation_summary.f90",
 "notebooks/person_situation_debate_notebook.ipynb"
]
required_cols = {
 "person_id","assessment_context","occasion","trait_score","trait_extraversion","trait_conscientiousness","trait_neuroticism",
 "state_extraversion","state_conscientiousness","state_assertiveness","state_withdrawal",
 "situation_demand","situation_sociality","situation_evaluation","situation_trust","situation_autonomy","situation_threat",
 "behavioral_consistency_marker","conditional_signature_score","state_inertia_marker"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_person_situation_data.csv"
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
