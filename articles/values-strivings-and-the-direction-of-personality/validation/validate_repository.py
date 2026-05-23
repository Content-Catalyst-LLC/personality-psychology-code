#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_values_strivings_direction.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_values_strivings_direction.py","r/analyze_values_strivings_direction.R","sql/schema_and_queries.sql",
 "julia/analyze_values_strivings_direction.jl","go/values_strivings_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/values_strivings_summary.c","cpp/values_strivings_summary.cpp","fortran/values_strivings_summary.f90",
 "notebooks/values_strivings_direction_notebook.ipynb"
]
required_cols = {
 "person_id","value_context","benevolence","universalism","self_direction","achievement","power","security","tradition","stimulation",
 "striving_meaning","striving_status","striving_care","striving_autonomy","striving_competence","striving_relatedness",
 "striving_conflict","striving_ownership","life_satisfaction","self_transcendence","self_enhancement","openness_to_change","conservation",
 "value_tension_self_transcendence_enhancement","value_tension_openness_conservation","value_tension_total",
 "striving_prosocial_orientation","motivational_quality","life_direction_coherence"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_values_strivings_direction.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 120: errors.append(f"Expected at least 120 rows, found {len(rows)}")
        contexts = {row.get("value_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 value contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
