#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required=(
  "README.md"
  "UPGRADE_MANIFEST.md"
  "data/synthetic_personality_creativity.csv"
  "data/data_dictionary.md"
  "data/provenance.md"
  "docs/methods.md"
  "docs/reproducibility.md"
  "docs/responsible-use.md"
  "python/analyze_personality_creativity.py"
  "r/analyze_personality_creativity.R"
  "sql/schema_and_queries.sql"
)

for path in "${required[@]}"; do
  if [ ! -f "$path" ]; then
    echo "Missing required file: $path" >&2
    exit 1
  fi
done

rows=$(($(wc -l < data/synthetic_personality_creativity.csv) - 1))
if [ "$rows" -lt 25 ]; then
  echo "Synthetic dataset has too few rows: $rows" >&2
  exit 1
fi

echo "Validation passed. Required scaffold files exist and dataset has $rows rows."
