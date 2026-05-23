#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_values_strivings_direction.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

VALUES = [
    "benevolence",
    "universalism",
    "self_direction",
    "achievement",
    "power",
    "security",
    "tradition",
    "stimulation",
]
STRIVINGS = [
    "striving_meaning",
    "striving_status",
    "striving_care",
    "striving_autonomy",
    "striving_competence",
    "striving_relatedness",
    "striving_conflict",
    "striving_ownership",
]
DERIVED = [
    "self_transcendence",
    "self_enhancement",
    "openness_to_change",
    "conservation",
    "value_tension_self_transcendence_enhancement",
    "value_tension_openness_conservation",
    "value_tension_total",
    "striving_prosocial_orientation",
    "motivational_quality",
    "life_direction_coherence",
]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "value_context", "life_satisfaction", *VALUES, *STRIVINGS, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["transcendence_level"] = np.where(df["self_transcendence"] > df["self_transcendence"].median(), "higher_transcendence", "lower_transcendence")
df["enhancement_level"] = np.where(df["self_enhancement"] > df["self_enhancement"].median(), "higher_enhancement", "lower_enhancement")
df["conflict_level"] = np.where(df["striving_conflict"] > df["striving_conflict"].median(), "higher_conflict", "lower_conflict")
df["direction_profile"] = df["transcendence_level"] + "_" + df["enhancement_level"] + "_" + df["conflict_level"]

df["high_conflict_low_ownership"] = (
    (df["striving_conflict"] > df["striving_conflict"].median())
    & (df["striving_ownership"] < df["striving_ownership"].median())
)
df["high_status_low_meaning"] = (
    (df["striving_status"] > df["striving_status"].median())
    & (df["striving_meaning"] < df["striving_meaning"].median())
)

context_summary = (
    df.groupby("value_context")
    .agg(
        n=("person_id", "count"),
        self_transcendence_mean=("self_transcendence", "mean"),
        self_enhancement_mean=("self_enhancement", "mean"),
        openness_to_change_mean=("openness_to_change", "mean"),
        conservation_mean=("conservation", "mean"),
        value_tension_mean=("value_tension_total", "mean"),
        motivational_quality_mean=("motivational_quality", "mean"),
        striving_conflict_mean=("striving_conflict", "mean"),
        life_direction_coherence_mean=("life_direction_coherence", "mean"),
        life_satisfaction_mean=("life_satisfaction", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("direction_profile")
    .agg(
        n=("person_id", "count"),
        self_transcendence_mean=("self_transcendence", "mean"),
        self_enhancement_mean=("self_enhancement", "mean"),
        motivational_quality_mean=("motivational_quality", "mean"),
        striving_conflict_mean=("striving_conflict", "mean"),
        life_direction_coherence_mean=("life_direction_coherence", "mean"),
        life_satisfaction_mean=("life_satisfaction", "mean"),
    )
    .reset_index()
)

pattern_summary = pd.DataFrame({
    "pattern": ["high_conflict_low_ownership", "high_status_low_meaning"],
    "n": [int(df["high_conflict_low_ownership"].sum()), int(df["high_status_low_meaning"].sum())],
    "proportion": [float(df["high_conflict_low_ownership"].mean()), float(df["high_status_low_meaning"].mean())],
})

models = {
    "life_satisfaction": ols(
        df,
        "life_satisfaction",
        [
            "self_transcendence",
            "self_enhancement",
            "openness_to_change",
            "conservation",
            "striving_meaning",
            "striving_status",
            "striving_care",
            "motivational_quality",
            "striving_conflict",
        ],
    ),
    "life_direction_coherence": ols(
        df,
        "life_direction_coherence",
        [
            "self_transcendence",
            "openness_to_change",
            "striving_ownership",
            "striving_conflict",
            "value_tension_total",
        ],
    ),
    "motivational_quality": ols(
        df,
        "motivational_quality",
        [
            "striving_autonomy",
            "striving_competence",
            "striving_relatedness",
            "striving_ownership",
            "striving_conflict",
        ],
    ),
    "note": "Synthetic demonstration only; not moral ranking, clinical assessment, personality testing, workplace screening, legal evaluation, or individual prediction.",
}

corr_cols = VALUES + STRIVINGS + DERIVED + ["life_satisfaction"]

context_summary.to_csv(OUT / "python_values_strivings_context_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_values_strivings_direction_profile_summary.csv", index=False)
pattern_summary.to_csv(OUT / "python_values_strivings_pattern_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_values_strivings_correlations.csv")
(OUT / "python_values_strivings_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_values_strivings_direction.csv", index=False)
print(f"Wrote outputs to {OUT}")
