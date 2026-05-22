#!/usr/bin/env python3
"""Analyze synthetic personality, wellbeing, and mental-health data.

This script supports the article "Personality, Wellbeing, and Mental Health."
It demonstrates age-band summaries, life-context summaries, trait-wellbeing
correlations, two-continua mental-health profiles, and regression-style models
using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_wellbeing_mental_health.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
]

PATHWAYS = [
    "coping_effectiveness",
    "perceived_support",
    "stress_burden",
    "treatment_access",
    "sleep_quality",
]

OUTCOMES = [
    "wellbeing_score",
    "distress_score",
    "flourishing_score",
    "social_functioning",
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
        "participant_id",
        "age_band",
        "life_context",
        *TRAITS,
        *PATHWAYS,
        "positive_affect",
        "negative_affect",
        "life_satisfaction",
        "meaning_purpose",
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["regulation_support_index"] = (
        df["conscientiousness"]
        + df["coping_effectiveness"]
        + df["perceived_support"]
        + df["sleep_quality"]
        - df["stress_burden"]
    ) / 4.0

    df["flourishing_capacity_index"] = (
        df["positive_affect"]
        + df["meaning_purpose"]
        + df["life_satisfaction"]
        + df["perceived_support"]
        - df["negative_affect"]
    ) / 4.0

    df["distress_vulnerability_index"] = (
        df["neuroticism"]
        + df["stress_burden"]
        + df["negative_affect"]
        - df["coping_effectiveness"]
        - df["perceived_support"]
    )

    df["distress_level"] = np.where(
        df["distress_score"] > df["distress_score"].median(),
        "higher_distress",
        "lower_distress",
    )

    df["flourishing_level"] = np.where(
        df["flourishing_score"] > df["flourishing_score"].median(),
        "higher_flourishing",
        "lower_flourishing",
    )

    df["mental_health_profile"] = (
        df["distress_level"] + "_" + df["flourishing_level"]
    )

    context_summary = (
        df.groupby("life_context")
        .agg(
            n=("participant_id", "count"),
            wellbeing_mean=("wellbeing_score", "mean"),
            distress_mean=("distress_score", "mean"),
            flourishing_mean=("flourishing_score", "mean"),
            support_mean=("perceived_support", "mean"),
            stress_burden_mean=("stress_burden", "mean"),
            treatment_access_mean=("treatment_access", "mean"),
        )
        .reset_index()
    )

    age_summary = (
        df.groupby("age_band")
        .agg(
            n=("participant_id", "count"),
            positive_affect_mean=("positive_affect", "mean"),
            negative_affect_mean=("negative_affect", "mean"),
            life_satisfaction_mean=("life_satisfaction", "mean"),
            meaning_purpose_mean=("meaning_purpose", "mean"),
            social_functioning_mean=("social_functioning", "mean"),
        )
        .reset_index()
    )

    profile_summary = (
        df.groupby("mental_health_profile")
        .agg(
            n=("participant_id", "count"),
            wellbeing_mean=("wellbeing_score", "mean"),
            distress_mean=("distress_score", "mean"),
            flourishing_mean=("flourishing_score", "mean"),
            neuroticism_mean=("neuroticism", "mean"),
            extraversion_mean=("extraversion", "mean"),
            conscientiousness_mean=("conscientiousness", "mean"),
            perceived_support_mean=("perceived_support", "mean"),
        )
        .reset_index()
    )

    context_summary.to_csv(OUTPUTS / "python_life_context_summary.csv", index=False)
    age_summary.to_csv(OUTPUTS / "python_age_band_summary.csv", index=False)
    profile_summary.to_csv(OUTPUTS / "python_two_continua_profile_summary.csv", index=False)

    corr_cols = TRAITS + PATHWAYS + [
        "positive_affect",
        "negative_affect",
        "life_satisfaction",
        "meaning_purpose",
        "regulation_support_index",
        "flourishing_capacity_index",
        "distress_vulnerability_index",
    ] + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_trait_wellbeing_correlations.csv")

    wellbeing_inputs = TRAITS + ["perceived_support", "coping_effectiveness", "sleep_quality"]
    distress_inputs = TRAITS + ["stress_burden", "perceived_support", "sleep_quality"]
    flourishing_inputs = TRAITS + ["meaning_purpose", "perceived_support", "coping_effectiveness"]
    functioning_inputs = ["extraversion", "agreeableness", "conscientiousness", "perceived_support", "distress_score", "sleep_quality"]

    models = {
        "wellbeing_score": fit_ols(df, "wellbeing_score", wellbeing_inputs),
        "distress_score": fit_ols(df, "distress_score", distress_inputs),
        "flourishing_score": fit_ols(df, "flourishing_score", flourishing_inputs),
        "social_functioning": fit_ols(df, "social_functioning", functioning_inputs),
        "note": "Synthetic demonstration only; not a clinical, diagnostic, or mental-health scoring model.",
    }

    with open(OUTPUTS / "python_personality_wellbeing_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_personality_wellbeing.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
