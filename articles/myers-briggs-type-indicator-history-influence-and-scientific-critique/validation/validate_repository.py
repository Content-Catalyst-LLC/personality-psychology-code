#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_mbti_typology_vs_traits.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_mbti_typology_vs_traits.py","r/analyze_mbti_typology_vs_traits.R","sql/schema_and_queries.sql",
 "julia/analyze_mbti_typology_vs_traits.jl","go/mbti_type_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/mbti_type_summary.c","cpp/mbti_type_summary.cpp","fortran/mbti_type_summary.f90",
 "notebooks/mbti_typology_vs_traits_notebook.ipynb"
]
required_cols = {
 "person_id","assessment_context","latent_ei","latent_sn","latent_tf","latent_jp",
 "observed_ei","observed_sn","observed_tf","observed_jp","retest_ei","retest_sn","retest_tf","retest_jp",
 "ei_letter","sn_letter","tf_letter","jp_letter","type_code","retest_type_code","type_changed_on_retest",
 "min_absolute_distance_to_boundary","near_boundary","continuous_signal_strength","boundary_risk_score",
 "information_loss_index","collaboration_score","reflective_utility_score"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_mbti_typology_vs_traits.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 600: errors.append(f"Expected at least 600 rows, found {len(rows)}")
        type_codes = {row.get("type_code") for row in rows}
        if len(type_codes) < 12: errors.append(f"Expected at least 12 type codes, found {len(type_codes)}")
        contexts = {row.get("assessment_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 assessment contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
