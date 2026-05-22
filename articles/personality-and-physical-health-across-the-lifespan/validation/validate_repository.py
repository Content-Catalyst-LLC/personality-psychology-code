#!/usr/bin/env python3
"""Validate the personality and physical health article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_physical_health_lifespan.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_personality_physical_health.py",
    "r/analyze_personality_physical_health.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_physical_health.jl",
    "go/health_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/health_summary.c",
    "cpp/health_summary.cpp",
    "fortran/health_summary.f90",
    "notebooks/personality_physical_health_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "person_id",
    "wave",
    "age",
    "age_band",
    "life_context",
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "emotional_stability",
    "perceived_support",
    "exercise",
    "sleep_quality",
    "smoking_risk",
    "alcohol_risk",
    "medication_adherence",
    "stress_burden",
    "physical_health_score",
    "functional_ability",
    "chronic_condition_burden",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_physical_health_lifespan.csv"
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
            age_bands = {row["age_band"] for row in rows if row.get("age_band")}
            contexts = {row["life_context"] for row in rows if row.get("life_context")}
            people = {row["person_id"] for row in rows if row.get("person_id")}
            waves = {row["wave"] for row in rows if row.get("wave")}
            if len(age_bands) < 4:
                errors.append(f"Expected at least 4 age bands, found {len(age_bands)}")
            if len(contexts) < 4:
                errors.append(f"Expected at least 4 life contexts, found {len(contexts)}")
            if len(people) < 50:
                errors.append(f"Expected at least 50 synthetic persons, found {len(people)}")
            if len(waves) < 3:
                errors.append(f"Expected at least 3 waves, found {len(waves)}")

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
