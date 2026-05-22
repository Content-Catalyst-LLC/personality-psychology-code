#!/usr/bin/env python3
"""Validate the article companion repository structure."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_culture_universality.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-use.md",
    "python/analyze_personality_culture_universality.py",
    "r/analyze_personality_culture_universality.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_culture_universality.jl",
    "go/matrix_similarity.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/trait_summary.c",
    "cpp/trait_summary.cpp",
    "fortran/trait_summary.f90",
    "notebooks/personality_culture_universality_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "culture_group",
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
    "honesty_humility",
    "context_collectivism",
    "behavioral_manifestation",
    "survey_language_family",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_culture_universality.csv"
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
            groups = {row["culture_group"] for row in rows if row.get("culture_group")}
            if len(groups) < 4:
                errors.append(f"Expected at least 4 culture groups, found {len(groups)}")

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
