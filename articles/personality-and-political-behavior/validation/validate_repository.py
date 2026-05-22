#!/usr/bin/env python3
"""Validate the personality and political behavior article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_political_behavior.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_personality_political_behavior.py",
    "r/analyze_personality_political_behavior.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_political_behavior.jl",
    "go/political_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/political_summary.c",
    "cpp/political_summary.cpp",
    "fortran/political_summary.f90",
    "notebooks/personality_political_behavior_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "country_context",
    "political_system_type",
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "political_interest",
    "political_efficacy",
    "group_identity_strength",
    "perceived_threat",
    "media_exposure",
    "civic_opportunity",
    "ideology_score",
    "political_participation",
    "affective_polarization",
    "trust_in_institutions",
    "leadership_authority_preference",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_political_behavior.csv"
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
            contexts = {row["country_context"] for row in rows if row.get("country_context")}
            if len(contexts) < 4:
                errors.append(f"Expected at least 4 country contexts, found {len(contexts)}")

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
