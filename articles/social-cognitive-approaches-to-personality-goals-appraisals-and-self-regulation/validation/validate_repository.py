#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_social_cognitive_personality.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_social_cognitive_personality.py","r/analyze_social_cognitive_personality.R","sql/schema_and_queries.sql",
 "julia/analyze_social_cognitive_personality.jl","go/social_cognitive_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/social_cognitive_summary.c","cpp/social_cognitive_summary.cpp","fortran/social_cognitive_summary.f90",
 "notebooks/social_cognitive_personality_notebook.ipynb"
]
required_cols = {
 "person_id","occasion","situation_type","goal_activation","threat_appraisal","challenge_appraisal","self_efficacy",
 "self_regulation","emotional_arousal","perceived_support","prosocial_behavior","avoidance_behavior","task_persistence",
 "appraisal_balance","regulation_capacity","approach_orientation","avoidance_pressure"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_social_cognitive_personality.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 200: errors.append(f"Expected at least 200 repeated-measures rows, found {len(rows)}")
        people = {row.get("person_id") for row in rows}
        if len(people) < 30: errors.append(f"Expected at least 30 synthetic people, found {len(people)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
