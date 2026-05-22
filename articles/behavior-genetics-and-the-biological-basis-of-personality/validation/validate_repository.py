#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_twin_data.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_behavior_genetics_personality.py","r/analyze_behavior_genetics_personality.R","sql/schema_and_queries.sql",
 "julia/analyze_behavior_genetics_personality.jl","go/behavior_genetics_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/behavior_genetics_summary.c","cpp/behavior_genetics_summary.cpp","fortran/behavior_genetics_summary.f90",
 "notebooks/behavior_genetics_personality_notebook.ipynb"
]
required_cols = {
 "pair_id","zygosity","genetic_relatedness","twin1_trait","twin2_trait",
 "twin1_temperament_reactivity","twin2_temperament_reactivity","twin1_effortful_control","twin2_effortful_control",
 "family_stress","social_support","socioeconomic_security","educational_stability",
 "shared_environment_index","nonshared_environment_index","trait_mean","trait_difference","gxe_marker","rge_marker","developmental_context_score"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_personality_twin_data.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 600: errors.append(f"Expected at least 600 synthetic twin pairs, found {len(rows)}")
        zyg = {row.get("zygosity") for row in rows}
        if not {"MZ","DZ"}.issubset(zyg): errors.append(f"Expected both MZ and DZ zygosity groups, found {sorted(zyg)}")
        pair_ids = {row.get("pair_id") for row in rows}
        if len(pair_ids) != len(rows): errors.append("pair_id values should be unique")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
