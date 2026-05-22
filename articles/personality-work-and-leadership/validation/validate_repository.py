#!/usr/bin/env python3
"""Validate the personality, work, and leadership article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_work_leadership.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_personality_work_leadership.py",
    "r/analyze_personality_work_leadership.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_work_leadership.jl",
    "go/work_leadership_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/work_leadership_summary.c",
    "cpp/work_leadership_summary.cpp",
    "fortran/work_leadership_summary.f90",
    "notebooks/personality_work_leadership_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "role_family",
    "organizational_context",
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "emotional_stability",
    "dark_trait_pressure",
    "role_fit",
    "accountability",
    "job_performance",
    "leadership_emergence",
    "leadership_effectiveness",
    "counterproductive_work_behavior",
    "teamwork_quality",
    "burnout_risk",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_work_leadership.csv"
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
            roles = {row["role_family"] for row in rows if row.get("role_family")}
            if len(roles) < 4:
                errors.append(f"Expected at least 4 role families, found {len(roles)}")

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
