#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_types_traits_dimensional_models.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_types_traits_dimensional_models.py","r/analyze_types_traits_dimensional_models.R","sql/schema_and_queries.sql",
 "julia/analyze_types_traits_dimensional_models.jl","go/type_trait_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/type_trait_summary.c","cpp/type_trait_summary.cpp","fortran/type_trait_summary.f90",
 "notebooks/types_traits_dimensional_models_notebook.ipynb"
]
required_cols = {
 "person_id","assessment_context","extraversion","agreeableness","conscientiousness","neuroticism","openness",
 "extraversion_category","conscientiousness_category","neuroticism_category","profile_type","synthetic_cluster",
 "nearest_threshold_distance","near_threshold_boundary","cluster_boundary_margin","near_cluster_boundary",
 "dimensional_signal_strength","information_loss_index","well_being","collaboration_score","reflective_utility_score"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_types_traits_dimensional_models.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 600: errors.append(f"Expected at least 600 rows, found {len(rows)}")
        profile_types = {row.get("profile_type") for row in rows}
        if len(profile_types) < 5: errors.append(f"Expected at least 5 profile types, found {len(profile_types)}")
        contexts = {row.get("assessment_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 assessment contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
