#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_selfhood_agency_identity.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_selfhood_agency_identity.py","r/analyze_selfhood_agency_identity.R","sql/schema_and_queries.sql",
 "julia/analyze_selfhood_agency_identity.jl","go/selfhood_agency_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/selfhood_agency_summary.c","cpp/selfhood_agency_summary.cpp","fortran/selfhood_agency_summary.f90",
 "notebooks/selfhood_agency_identity_notebook.ipynb"
]
required_cols = {
 "person_id","identity_context","past_self","present_self","future_self","intentional_clarity","action_ownership",
 "self_efficacy","external_constraint","social_recognition","value_commitment_gap","identity_integration","well_being",
 "past_present_gap","present_future_gap","temporal_self_continuity","agency_index","situated_agency_index","identity_alignment"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_selfhood_agency_identity.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 120: errors.append(f"Expected at least 120 rows, found {len(rows)}")
        contexts = {row.get("identity_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 identity contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
