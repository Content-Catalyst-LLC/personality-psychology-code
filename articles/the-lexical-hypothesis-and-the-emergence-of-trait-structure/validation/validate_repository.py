#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_lexical_descriptors.csv","data/synthetic_lexical_scores_for_sql.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_lexical_structure.py","r/analyze_lexical_structure.R","sql/schema_and_queries.sql",
 "julia/analyze_lexical_structure.jl","go/lexical_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/lexical_summary.c","cpp/lexical_summary.cpp","fortran/lexical_summary.f90",
 "notebooks/lexical_structure_notebook.ipynb"
]
required_cols = {
 "respondent_id", *[f"adj{i}" for i in range(1,101)],
 "sociable_cluster_score","reliable_cluster_score","compassionate_cluster_score","anxious_cluster_score","imaginative_cluster_score",
 "social_reliability_outcome","interpersonal_trust_outcome","expressive_engagement_outcome","lexical_visibility_index",
 "lexical_abundance_index","structural_centrality_index","descriptor_redundancy_index","cross_language_caution_index"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_lexical_descriptors.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 800: errors.append(f"Expected at least 800 synthetic respondents, found {len(rows)}")
        respondent_ids = {row.get("respondent_id") for row in rows}
        if len(respondent_ids) != len(rows): errors.append("respondent_id values should be unique")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
