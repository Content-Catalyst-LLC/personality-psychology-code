#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_maladaptive_personality_structure.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_maladaptive_personality.py","r/analyze_maladaptive_personality.R","sql/schema_and_queries.sql",
 "julia/analyze_maladaptive_personality.jl","go/maladaptive_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/maladaptive_summary.c","cpp/maladaptive_summary.cpp","fortran/maladaptive_summary.f90",
 "notebooks/maladaptive_personality_notebook.ipynb"
]
required_cols = {
 "participant_id","clinical_context","negative_affectivity","detachment","antagonism","disinhibition","psychoticism","anankastia",
 "identity_impairment","self_direction_impairment","empathy_impairment","intimacy_impairment",
 "self_functioning_impairment","interpersonal_functioning_impairment","functioning_impairment",
 "maladaptive_trait_burden","severity_trait_interaction","rigidity","pervasiveness","contextual_stress","perceived_support",
 "clinical_severity","clinical_liability","threshold_zone_indicator"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_maladaptive_personality_structure.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 100: errors.append(f"Expected at least 100 rows, found {len(rows)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
