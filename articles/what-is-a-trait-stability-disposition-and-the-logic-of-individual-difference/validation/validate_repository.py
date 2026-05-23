#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_trait_items.csv","data/synthetic_state_observations.csv","data/synthetic_trait_state_summary_for_sql.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/professional-use-boundary.md","docs/responsible-interpretation.md",
 "python/analyze_trait_stability.py","r/analyze_trait_stability.R","sql/schema_and_queries.sql",
 "julia/analyze_trait_stability.jl","go/trait_stability_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/trait_stability_summary.c","cpp/trait_stability_summary.cpp","fortran/trait_stability_summary.f90",
 "notebooks/trait_stability_notebook.ipynb"
]
trait_cols = {"person_id", *[f"c{i}" for i in range(1,7)], *[f"e{i}" for i in range(1,7)], *[f"n{i}" for i in range(1,7)], "conscientiousness_score", "extraversion_score", "neuroticism_score", "self_report_consistency_index", "trait_observation_alignment"}
state_cols = {"person_id", "occasion", "situation_type", "state_extraversion", "state_conscientiousness", "state_neuroticism", "situational_activation", "situational_constraint"}
summary_cols = {"person_id", "conscientiousness_score", "extraversion_score", "neuroticism_score", "mean_state_conscientiousness", "sd_state_conscientiousness", "mean_state_extraversion", "sd_state_extraversion", "mean_state_neuroticism", "sd_state_neuroticism", "n_observations", "trait_state_alignment_index", "state_variability_index", "person_situation_sensitivity_index", "aggregation_reliability_index"}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]

def check_csv(path, required, min_rows):
    if not path.exists():
        return
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required - set(reader.fieldnames or [])
        if missing:
            errors.append(f"{path.name} missing columns: {sorted(missing)}")
        if len(rows) < min_rows:
            errors.append(f"{path.name} expected at least {min_rows} rows, found {len(rows)}")

check_csv(ROOT / "data" / "synthetic_trait_items.csv", trait_cols, 700)
check_csv(ROOT / "data" / "synthetic_state_observations.csv", state_cols, 10000)
check_csv(ROOT / "data" / "synthetic_trait_state_summary_for_sql.csv", summary_cols, 700)

if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
