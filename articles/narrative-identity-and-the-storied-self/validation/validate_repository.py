#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_narrative_identity.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_narrative_identity.py","r/analyze_narrative_identity.R","sql/schema_and_queries.sql",
 "julia/analyze_narrative_identity.jl","go/narrative_identity_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/narrative_identity_summary.c","cpp/narrative_identity_summary.cpp","fortran/narrative_identity_summary.f90",
 "notebooks/narrative_identity_notebook.ipynb"
]
required_cols = {
 "person_id","narrative_context","redemption","contamination","coherence","agency","communion","meaning_making",
 "narrative_flexibility","defensive_rigidity","self_continuity","well_being","narrative_growth_orientation",
 "narrative_burden","narrative_integration","redemptive_agency_balance"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_narrative_identity.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 120: errors.append(f"Expected at least 120 rows, found {len(rows)}")
        contexts = {row.get("narrative_context") for row in rows}
        if len(contexts) < 5: errors.append(f"Expected at least 5 narrative contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
