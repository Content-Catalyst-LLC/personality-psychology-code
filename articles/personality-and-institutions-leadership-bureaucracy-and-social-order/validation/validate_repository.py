#!/usr/bin/env python3
"""Validate the institutional-personality article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_institutions_bureaucracy.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_personality_institutions.py",
    "r/analyze_personality_institutions.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_institutions.jl",
    "go/institutional_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/institutional_summary.c",
    "cpp/institutional_summary.cpp",
    "fortran/institutional_summary.f90",
    "notebooks/personality_institutions_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "institutional_unit",
    "role_type",
    "conscientiousness",
    "agreeableness",
    "emotional_stability",
    "openness",
    "dark_trait_pressure",
    "bureaucratic_fit",
    "discretion_level",
    "accountability_strength",
    "leadership_rating",
    "institutional_performance",
    "institutional_trust",
    "role_clarity",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_institutions_bureaucracy.csv"
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
            units = {row["institutional_unit"] for row in rows if row.get("institutional_unit")}
            if len(units) < 4:
                errors.append(f"Expected at least 4 institutional units, found {len(units)}")

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
