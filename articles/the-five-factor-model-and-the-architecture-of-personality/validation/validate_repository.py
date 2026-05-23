#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_ffm_items.csv","data/synthetic_ffm_scores_for_sql.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_ffm_architecture.py","r/analyze_ffm_architecture.R","sql/schema_and_queries.sql",
 "julia/analyze_ffm_architecture.jl","go/ffm_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/ffm_summary.c","cpp/ffm_summary.cpp","fortran/ffm_summary.f90",
 "notebooks/ffm_architecture_notebook.ipynb"
]
required_cols = {
 "respondent_id", *[f"item{i}" for i in range(1,61)], "c1","c2","c3","c4","c5","c6","o1","o2","o3","i1","i2","i3",
 "extraversion_score","agreeableness_score","conscientiousness_score","neuroticism_score","openness_score",
 "sociability_score","assertiveness_score","compassion_score","politeness_score","orderliness_score","industriousness_score",
 "anxiety_score","volatility_score","aesthetics_score","intellect_score",
 "outcome_score","broad_life_functioning","relationship_functioning","creative_engagement","emotional_distress",
 "facet_profile_dispersion","hierarchy_consistency_index","bandwidth_fidelity_gap","domain_facet_alignment"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_ffm_items.csv"
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
