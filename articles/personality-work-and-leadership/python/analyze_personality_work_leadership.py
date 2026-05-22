#!/usr/bin/env python3
"""Analyze synthetic personality, work, and leadership data.

This script supports the article "Personality, Work, and Leadership." It
demonstrates role-family summaries, organizational-context summaries, trait
correlations, performance and leadership models, and stewardship / derailment
indices using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_work_leadership.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "emotional_stability",
    "dark_trait_pressure",
]

OUTCOMES = [
    "job_performance",
    "leadership_emergence",
    "leadership_effectiveness",
    "counterproductive_work_behavior",
    "teamwork_quality",
    "burnout_risk",
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
        "role_family",
        "organizational_context",
        *TRAITS,
        "role_fit",
        "accountability",
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["dependability_index"] = (
        df["conscientiousness"]
        + df["emotional_stability"]
        + df["role_fit"]
    ) / 3.0

    df["leadership_stewardship_index"] = (
        df["conscientiousness"]
        + df["agreeableness"]
        + df["emotional_stability"]
        + df["accountability"]
        - df["dark_trait_pressure"]
    ) / 4.0

    df["derailment_risk_index"] = (
        df["dark_trait_pressure"]
        + df["neuroticism"]
        - df["accountability"]
        - df["role_fit"]
    )

    role_summary = (
        df.groupby("role_family")
        .agg(
            n=("participant_id", "count"),
            performance_mean=("job_performance", "mean"),
            leadership_emergence_mean=("leadership_emergence", "mean"),
            leadership_effectiveness_mean=("leadership_effectiveness", "mean"),
            teamwork_mean=("teamwork_quality", "mean"),
            burnout_risk_mean=("burnout_risk", "mean"),
            stewardship_mean=("leadership_stewardship_index", "mean"),
            derailment_risk_mean=("derailment_risk_index", "mean"),
        )
        .reset_index()
    )

    context_summary = (
        df.groupby("organizational_context")
        .agg(
            n=("participant_id", "count"),
            role_fit_mean=("role_fit", "mean"),
            accountability_mean=("accountability", "mean"),
            performance_mean=("job_performance", "mean"),
            cwb_mean=("counterproductive_work_behavior", "mean"),
            burnout_risk_mean=("burnout_risk", "mean"),
        )
        .reset_index()
    )

    role_summary.to_csv(OUTPUTS / "python_role_family_summary.csv", index=False)
    context_summary.to_csv(OUTPUTS / "python_organizational_context_summary.csv", index=False)

    corr_cols = TRAITS + [
        "role_fit",
        "accountability",
        "dependability_index",
        "leadership_stewardship_index",
        "derailment_risk_index",
    ] + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_trait_work_correlations.csv")

    performance_inputs = ["extraversion", "agreeableness", "conscientiousness", "emotional_stability", "openness", "role_fit"]
    emergence_inputs = ["extraversion", "openness", "emotional_stability", "role_fit"]
    effectiveness_inputs = ["conscientiousness", "agreeableness", "emotional_stability", "openness", "role_fit", "accountability"]
    cwb_inputs = ["dark_trait_pressure", "neuroticism", "agreeableness", "conscientiousness", "accountability"]

    models = {
        "job_performance": fit_ols(df, "job_performance", performance_inputs),
        "leadership_emergence": fit_ols(df, "leadership_emergence", emergence_inputs),
        "leadership_effectiveness": fit_ols(df, "leadership_effectiveness", effectiveness_inputs),
        "counterproductive_work_behavior": fit_ols(df, "counterproductive_work_behavior", cwb_inputs),
        "note": "Synthetic demonstration only; not a workplace-screening or leadership-selection model.",
    }

    with open(OUTPUTS / "python_work_leadership_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_personality_work_leadership.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
