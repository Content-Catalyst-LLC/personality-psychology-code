#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_self_concept_self_esteem_self_knowledge.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_self_concept_self_esteem_self_knowledge.py","r/analyze_self_concept_self_esteem_self_knowledge.R","sql/schema_and_queries.sql",
 "julia/analyze_self_concept_self_esteem_self_knowledge.jl","go/self_system_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/self_system_summary.c","cpp/self_system_summary.cpp","fortran/self_system_summary.f90",
 "notebooks/self_concept_self_esteem_self_knowledge_notebook.ipynb"
]
required_cols = {
 "person_id","self_system_context","self_warmth","self_conscientiousness","self_emotional_stability","self_openness",
 "other_warmth","other_conscientiousness","other_emotional_stability","other_openness","actual_self","ideal_self","ought_self",
 "self_esteem","social_recognition","external_devaluation","well_being","warmth_gap","conscientiousness_gap",
 "emotional_stability_gap","openness_gap","self_other_gap_mean","self_knowledge_accuracy","actual_ideal_discrepancy",
 "actual_ought_discrepancy","total_self_discrepancy","self_concept_positivity"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_self_concept_self_esteem_self_knowledge.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 120: errors.append(f"Expected at least 120 rows, found {len(rows)}")
        contexts = {row.get("self_system_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 self-system contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
