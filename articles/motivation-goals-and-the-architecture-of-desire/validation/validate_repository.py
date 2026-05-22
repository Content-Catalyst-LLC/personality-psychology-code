#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_motivation_goals_desire.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_motivation_goals_desire.py","r/analyze_motivation_goals_desire.R","sql/schema_and_queries.sql",
 "julia/analyze_motivation_goals_desire.jl","go/motivation_goals_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/motivation_goals_summary.c","cpp/motivation_goals_summary.cpp","fortran/motivation_goals_summary.f90",
 "notebooks/motivation_goals_desire_notebook.ipynb"
]
required_cols = {
 "person_id","motivation_context","autonomy_goal","achievement_goal","belonging_goal","security_goal","meaning_goal","status_goal",
 "goal_conflict","goal_ownership","autonomy_support","competence_support","relatedness_support","conscientiousness",
 "persistence_score","adaptive_disengagement","well_being","total_goal_intensity","approach_orientation",
 "avoidance_security_orientation","status_orientation","need_support","motivational_quality","life_direction_coherence"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_motivation_goals_desire.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 120: errors.append(f"Expected at least 120 rows, found {len(rows)}")
        contexts = {row.get("motivation_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 motivation contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
