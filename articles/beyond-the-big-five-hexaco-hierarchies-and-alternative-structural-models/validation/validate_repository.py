#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_alternative_structure_items.csv","data/synthetic_alternative_structure_scores_for_sql.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_alternative_structures.py","r/analyze_alternative_structures.R","sql/schema_and_queries.sql",
 "julia/analyze_alternative_structures.jl","go/alternative_structure_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/alternative_structure_summary.c","cpp/alternative_structure_summary.cpp","fortran/alternative_structure_summary.f90",
 "notebooks/alternative_structures_notebook.ipynb"
]
required_cols = {
 "respondent_id", *[f"item{i}" for i in range(1,73)],
 "bf_extraversion","bf_agreeableness","bf_conscientiousness","bf_neuroticism","bf_openness",
 "hx_honesty_humility","hx_emotionality","hx_extraversion","hx_agreeableness","hx_conscientiousness","hx_openness",
 "sincerity_facet","fairness_facet","greed_avoidance_facet","modesty_facet","patience_facet","forgiveness_facet","anxiety_facet","sentimentality_facet",
 "outcome_integrity","outcome_interpersonal_trust","outcome_broad_functioning","outcome_exploitative_risk",
 "hexaco_increment_marker","repartitioning_gap","structural_comparison_index","facet_granularity_index"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_alternative_structure_items.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 700: errors.append(f"Expected at least 700 synthetic respondents, found {len(rows)}")
        respondent_ids = {row.get("respondent_id") for row in rows}
        if len(respondent_ids) != len(rows): errors.append("respondent_id values should be unique")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
