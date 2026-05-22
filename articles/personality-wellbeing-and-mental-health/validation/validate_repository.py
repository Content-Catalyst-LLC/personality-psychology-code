#!/usr/bin/env python3
"""Validate the personality, wellbeing, and mental-health article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_wellbeing_mental_health.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_personality_wellbeing.py",
    "r/analyze_personality_wellbeing.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_wellbeing.jl",
    "go/wellbeing_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/wellbeing_summary.c",
    "cpp/wellbeing_summary.cpp",
    "fortran/wellbeing_summary.f90",
    "notebooks/personality_wellbeing_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "age_band",
    "life_context",
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "coping_effectiveness",
    "perceived_support",
    "stress_burden",
    "positive_affect",
    "negative_affect",
    "life_satisfaction",
    "meaning_purpose",
    "wellbeing_score",
    "distress_score",
    "flourishing_score",
    "social_functioning",
    "treatment_access",
    "sleep_quality",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_wellbeing_mental_health.csv"
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
            contexts = {row["life_context"] for row in rows if row.get("life_context")}
            age_bands = {row["age_band"] for row in rows if row.get("age_band")}
            if len(contexts) < 4:
                errors.append(f"Expected at least 4 life contexts, found {len(contexts)}")
            if len(age_bands) < 4:
                errors.append(f"Expected at least 4 age bands, found {len(age_bands)}")

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
