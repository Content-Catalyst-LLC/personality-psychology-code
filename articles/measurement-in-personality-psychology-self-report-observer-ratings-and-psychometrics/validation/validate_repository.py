#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_measurement_data.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_personality_measurement_psychometrics.py","r/analyze_personality_measurement_psychometrics.R","sql/schema_and_queries.sql",
 "julia/analyze_personality_measurement_psychometrics.jl","go/measurement_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/measurement_summary.c","cpp/measurement_summary.cpp","fortran/measurement_summary.f90",
 "notebooks/personality_measurement_psychometrics_notebook.ipynb"
]
required_cols = {
 "person_id","assessment_context","s1","s2","s3","s4","s5","o1","o2","o3","o4","o5",
 "attention_check","careless_response_risk","social_desirability_pressure","self_missing_count","observer_missing_count",
 "self_conscientiousness","observer_conscientiousness","self_other_discrepancy","absolute_self_other_discrepancy",
 "method_effect_index","reliability_context_score","professional_reflection_score"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_personality_measurement_data.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 300: errors.append(f"Expected at least 300 rows, found {len(rows)}")
        contexts = {row.get("assessment_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 assessment contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
