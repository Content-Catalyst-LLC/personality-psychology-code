#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_history_items.csv","data/synthetic_personality_history_scores_for_sql.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_personality_history.py","r/analyze_personality_history.R","sql/schema_and_queries.sql",
 "julia/analyze_personality_history.jl","go/personality_history_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/personality_history_summary.c","cpp/personality_history_summary.cpp","fortran/personality_history_summary.f90",
 "notebooks/personality_history_notebook.ipynb"
]
required_cols = {
 "participant_id", *[f"item{i}" for i in range(1,61)], *[f"c{i}" for i in range(1,7)],
 "extraversion_score","agreeableness_score","conscientiousness_score","neuroticism_score","openness_score",
 "conscientiousness_t1","conscientiousness_t2","behavior_score","trait_score","situation_strength","person_situation_interaction",
 "characterology_typology_index","psychometric_structure_index","person_situation_index","narrative_identity_index","measurement_invariance_caution_index","historical_method_maturity_index"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_personality_history_items.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 800: errors.append(f"Expected at least 800 synthetic participants, found {len(rows)}")
        participant_ids = {row.get("participant_id") for row in rows}
        if len(participant_ids) != len(rows): errors.append("participant_id values should be unique")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
