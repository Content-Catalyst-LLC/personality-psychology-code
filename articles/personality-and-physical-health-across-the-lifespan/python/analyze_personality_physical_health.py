#!/usr/bin/env python3
"""Analyze synthetic personality and physical health data.

This script supports the article "Personality and Physical Health Across the
Lifespan." It demonstrates age-band summaries, life-context summaries,
trait-health correlations, behavior / stress indices, and simple regression-style
models using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_physical_health_lifespan.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "emotional_stability",
]

BEHAVIORS = [
    "exercise",
    "sleep_quality",
    "smoking_risk",
    "alcohol_risk",
    "medication_adherence",
]

OUTCOMES = [
    "physical_health_score",
    "functional_ability",
    "chronic_condition_burden",
]


def fit_ols(df: pd.DataFrame, y_col: str, x_cols: list[str]) -> dict[str, float]:
    """Fit a small OLS model with numpy and return coefficients."""
    X = df[x_cols].to_numpy(dtype=float)
    X = np.column_stack([np.ones(len(X)), X])
    y = df[y_col].to_numpy(dtype=float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    names = ["intercept", *x_cols]
    return {name: float(value) for name, value in zip(names, beta)}


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    required = {
        "person_id",
        "wave",
        "age",
        "age_band",
        "life_context",
        *TRAITS,
        "perceived_support",
        *BEHAVIORS,
        "stress_burden",
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["health_behavior_index"] = (
        df["exercise"]
        + df["sleep_quality"]
        + df["medication_adherence"]
        - df["smoking_risk"]
        - df["alcohol_risk"]
    ) / 3.0

    df["stress_vulnerability_index"] = (
        df["neuroticism"]
        + df["stress_burden"]
        - df["emotional_stability"]
        - df["perceived_support"]
    )

    df["healthy_aging_support_index"] = (
        df["physical_health_score"]
        + df["functional_ability"]
        + df["perceived_support"]
        + df["medication_adherence"]
    ) / 4.0

    df["healthy_neuroticism_index"] = (
        df["neuroticism"] * df["conscientiousness"]
    ) / 7.0

    age_summary = (
        df.groupby("age_band")
        .agg(
            observations=("person_id", "count"),
            mean_age=("age", "mean"),
            physical_health_mean=("physical_health_score", "mean"),
            functional_ability_mean=("functional_ability", "mean"),
            chronic_condition_burden_mean=("chronic_condition_burden", "mean"),
            health_behavior_mean=("health_behavior_index", "mean"),
            stress_vulnerability_mean=("stress_vulnerability_index", "mean"),
        )
        .reset_index()
        .sort_values("mean_age")
    )

    context_summary = (
        df.groupby("life_context")
        .agg(
            observations=("person_id", "count"),
            perceived_support_mean=("perceived_support", "mean"),
            medication_adherence_mean=("medication_adherence", "mean"),
            stress_burden_mean=("stress_burden", "mean"),
            physical_health_mean=("physical_health_score", "mean"),
            functional_ability_mean=("functional_ability", "mean"),
        )
        .reset_index()
    )

    age_summary.to_csv(OUTPUTS / "python_age_band_summary.csv", index=False)
    context_summary.to_csv(OUTPUTS / "python_life_context_summary.csv", index=False)

    corr_cols = TRAITS + [
        "perceived_support",
        "stress_burden",
        "health_behavior_index",
        "stress_vulnerability_index",
        "healthy_aging_support_index",
        "healthy_neuroticism_index",
    ] + BEHAVIORS + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_trait_health_correlations.csv")

    health_inputs = [
        "conscientiousness",
        "neuroticism",
        "extraversion",
        "openness",
        "exercise",
        "sleep_quality",
        "smoking_risk",
        "medication_adherence",
        "stress_burden",
        "age",
        "wave",
    ]

    healthy_neuroticism_inputs = [
        "neuroticism",
        "conscientiousness",
        "healthy_neuroticism_index",
        "exercise",
        "sleep_quality",
        "smoking_risk",
        "medication_adherence",
        "stress_burden",
        "age",
        "wave",
    ]

    function_inputs = [
        "physical_health_score",
        "conscientiousness",
        "emotional_stability",
        "perceived_support",
        "medication_adherence",
        "age",
        "wave",
    ]

    chronic_inputs = [
        "age",
        "stress_burden",
        "smoking_risk",
        "alcohol_risk",
        "conscientiousness",
        "physical_health_score",
        "perceived_support",
    ]

    models = {
        "physical_health_score": fit_ols(df, "physical_health_score", health_inputs),
        "healthy_neuroticism_model": fit_ols(df, "physical_health_score", healthy_neuroticism_inputs),
        "functional_ability": fit_ols(df, "functional_ability", function_inputs),
        "chronic_condition_burden": fit_ols(df, "chronic_condition_burden", chronic_inputs),
        "note": "Synthetic demonstration only; not a clinical prediction or public-health scoring model.",
    }

    with open(OUTPUTS / "python_personality_health_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_personality_physical_health.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
