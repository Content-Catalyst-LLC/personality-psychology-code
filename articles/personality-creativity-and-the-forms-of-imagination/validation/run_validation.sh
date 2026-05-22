#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ARTICLE_DIR"

echo "Validating article directory: $ARTICLE_DIR"

required_files=(
  "README.md"
  "data/synthetic_personality_creativity.csv"
  "data/data_dictionary.md"
  "data/provenance.md"
  "docs/methods.md"
  "docs/reproducibility.md"
  "docs/responsible-use.md"
  "python/analyze_personality_creativity.py"
  "r/analyze_personality_creativity.R"
  "sql/schema_and_queries.sql"
  "julia/analyze_personality_creativity.jl"
  "go/main.go"
  "rust/Cargo.toml"
  "rust/src/main.rs"
  "c/summary.c"
  "cpp/summary.cpp"
  "fortran/summary.f90"
  "notebooks/personality_creativity_analysis.ipynb"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "Missing required file: $file"
    exit 1
  fi
done

echo "Required file check passed."

row_count="$(awk 'END {print NR-1}' data/synthetic_personality_creativity.csv)"
if [ "$row_count" -lt 30 ]; then
  echo "Expected at least 30 synthetic data rows, found $row_count"
  exit 1
fi

echo "Synthetic dataset row check passed: $row_count rows."

if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY'
import csv
from pathlib import Path

path = Path("data/synthetic_personality_creativity.csv")
required = {
    "participant_id",
    "domain",
    "openness",
    "intellect",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
    "persistence",
    "social_support",
    "divergent_thinking",
    "creative_achievement",
    "everyday_creativity",
}

with path.open(newline="") as f:
    reader = csv.DictReader(f)
    missing = required.difference(reader.fieldnames or [])
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")
    rows = list(reader)

if len(rows) < 30:
    raise SystemExit("Expected at least 30 rows.")

print("Python CSV validation passed.")
PY
else
  echo "python3 not found; skipped Python CSV validation."
fi

echo "Validation complete."
