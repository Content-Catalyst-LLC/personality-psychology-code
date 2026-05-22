#!/usr/bin/env python3
"""Validate the personality, relationships, and social functioning article companion repository."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "UPGRADE_MANIFEST.md",
    "Makefile",
    "config/analysis_config.yml",
    "data/synthetic_personality_relationships_social_functioning.csv",
    "data/data_dictionary.md",
    "data/provenance.md",
    "docs/methods.md",
    "docs/reproducibility.md",
    "docs/responsible-research-use.md",
    "python/analyze_personality_relationships.py",
    "r/analyze_personality_relationships.R",
    "sql/schema_and_queries.sql",
    "julia/analyze_personality_relationships.jl",
    "go/relationships_summary.go",
    "rust/Cargo.toml",
    "rust/src/main.rs",
    "c/relationships_summary.c",
    "cpp/relationships_summary.cpp",
    "fortran/relationships_summary.f90",
    "notebooks/personality_relationships_notebook.ipynb",
]

REQUIRED_COLUMNS = {
    "participant_id",
    "social_context",
    "relationship_domain",
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "empathy",
    "self_regulation",
    "attachment_security",
    "perceived_support",
    "relationship_satisfaction",
    "social_functioning",
    "loneliness",
    "conflict_frequency",
    "reciprocity_quality",
    "reputation_trust",
}


def main() -> int:
    errors = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing file: {rel}")

    data_path = ROOT / "data" / "synthetic_personality_relationships_social_functioning.csv"
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
            contexts = {row["social_context"] for row in rows if row.get("social_context")}
            domains = {row["relationship_domain"] for row in rows if row.get("relationship_domain")}
            if len(contexts) < 4:
                errors.append(f"Expected at least 4 social contexts, found {len(contexts)}")
            if len(domains) < 4:
                errors.append(f"Expected at least 4 relationship domains, found {len(domains)}")

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
