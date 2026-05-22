#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_psychodynamic_personality.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_psychodynamic_personality.py","r/analyze_psychodynamic_personality.R","sql/schema_and_queries.sql",
 "julia/analyze_psychodynamic_personality.jl","go/psychodynamic_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/psychodynamic_summary.c","cpp/psychodynamic_summary.cpp","fortran/psychodynamic_summary.f90",
 "notebooks/psychodynamic_personality_notebook.ipynb"
]
required_cols = {
 "person_id","developmental_context","mature_defenses","neurotic_defenses","immature_defenses","defensive_rigidity",
 "attachment_anxiety","attachment_avoidance","self_cohesion","relational_security","reflective_functioning",
 "character_integration","symptom_distress","defensive_maturity","attachment_insecurity",
 "self_relational_capacity","hidden_structure_risk"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_psychodynamic_personality.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 100: errors.append(f"Expected at least 100 rows, found {len(rows)}")
        contexts = {row.get("developmental_context") for row in rows}
        if len(contexts) < 4: errors.append(f"Expected at least 4 developmental contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
