#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_temperament_personality_longitudinal.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_temperament_personality.py","r/analyze_temperament_personality.R","sql/schema_and_queries.sql",
 "julia/analyze_temperament_personality.jl","go/temperament_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/temperament_summary.c","cpp/temperament_summary.cpp","fortran/temperament_summary.f90",
 "notebooks/temperament_personality_notebook.ipynb"
]
required_cols = {
 "child_id","developmental_context","inhibition_t1","negative_affect_t1","surgency_t1","effortful_control_t1",
 "parenting_support_t1","family_stress_t1","classroom_support_t2","peer_support_t2","institutional_stability_t2",
 "conscientiousness_t2","neuroticism_t2","social_confidence_t2","regulation_skill_t2",
 "reactivity_regulation_balance","environmental_support_index","developmental_risk_index","adaptive_pathway_score"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_temperament_personality_longitudinal.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 500: errors.append(f"Expected at least 500 synthetic longitudinal rows, found {len(rows)}")
        contexts = {row.get("developmental_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 developmental contexts, found {len(contexts)}")
        child_ids = {row.get("child_id") for row in rows}
        if len(child_ids) != len(rows): errors.append("child_id values should be unique")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
