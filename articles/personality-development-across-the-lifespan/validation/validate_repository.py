#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
required_files = [
 "README.md","UPGRADE_MANIFEST.md","Makefile","config/analysis_config.yml",
 "data/synthetic_personality_lifespan.csv","data/data_dictionary.md","data/provenance.md",
 "docs/methods.md","docs/reproducibility.md","docs/responsible-research-use.md",
 "python/analyze_personality_lifespan.py","r/analyze_personality_lifespan.R","sql/schema_and_queries.sql",
 "julia/analyze_personality_lifespan.jl","go/personality_lifespan_summary.go","rust/Cargo.toml","rust/src/main.rs",
 "c/personality_lifespan_summary.c","cpp/personality_lifespan_summary.cpp","fortran/personality_lifespan_summary.f90",
 "notebooks/personality_lifespan_notebook.ipynb"
]
required_cols = {
 "person_id","wave","wave_numeric","age","life_stage","cohort","cultural_context","neuroticism","extraversion",
 "conscientiousness","openness","agreeableness","role_investment","state_practice_frequency","perceived_support"
}
errors = [f"Missing file: {f}" for f in required_files if not (ROOT / f).exists()]
data = ROOT / "data" / "synthetic_personality_lifespan.csv"
if data.exists():
    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        missing = required_cols - set(reader.fieldnames or [])
        if missing: errors.append(f"Dataset missing columns: {sorted(missing)}")
        if len(rows) < 500: errors.append(f"Expected at least 500 longitudinal rows, found {len(rows)}")
        people = {row.get("person_id") for row in rows}
        waves = {row.get("wave_numeric") for row in rows}
        stages = {row.get("life_stage") for row in rows}
        cohorts = {row.get("cohort") for row in rows}
        contexts = {row.get("cultural_context") for row in rows}
        if len(people) < 80: errors.append(f"Expected at least 80 synthetic people, found {len(people)}")
        if len(waves) < 6: errors.append(f"Expected at least 6 waves, found {len(waves)}")
        if len(stages) < 6: errors.append(f"Expected at least 6 life stages, found {len(stages)}")
        if len(cohorts) < 3: errors.append(f"Expected at least 3 cohorts, found {len(cohorts)}")
        if len(contexts) < 3: errors.append(f"Expected at least 3 cultural contexts, found {len(contexts)}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print("VALIDATION PASSED")
