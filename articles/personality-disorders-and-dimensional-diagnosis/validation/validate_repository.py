#!/usr/bin/env python3
"""Validate the personality disorders and dimensional diagnosis article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_disorders_dimensional_diagnosis.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_dimensional_personality_disorders.py",
    "r/analyze_dimensional_personality_disorders.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_dimensional_personality_disorders.jl",
    "go/dimensional_pd_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/dimensional_pd_summary.c",
    "cpp/dimensional_pd_summary.cpp",
    "fortran/dimensional_pd_summary.f90",
    "notebooks/dimensional_personality_disorders_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "clinical_context",
    "negative_affectivity",
    "detachment",
    "antagonism",
    "disinhibition",
    "psychoticism",
    "anankastia",
    "identity_impairment",
    "self_direction_impairment",
    "empathy_impairment",
    "intimacy_impairment",
    "self_functioning",
    "interpersonal_functioning",
    "functioning_impairment",
    "maladaptive_trait_burden",
    "severity_trait_interaction",
    "borderline_pattern_indicator",
    "pd_severity",
    "risk_level",
    "treatment_engagement",
    "perceived_support",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_disorders_dimensional_diagnosis.csv"
    if data_path.exists():
        with data_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns
            if missing:
                errors.append(f"Dataset missing columns: {sorted(missing)}")
            rows = list(reader)
            if len(rows) < 100:
                errors.append(f"Expected at least 100 synthetic rows, found {len(rows)}")
            contexts = {row["clinical_context"] for row in rows if row.get("clinical_context")}
            if len(contexts) < 4:
                errors.append(f"Expected at least 4 clinical contexts, found {len(contexts)}")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED")
    print(f"Checked repository: {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
