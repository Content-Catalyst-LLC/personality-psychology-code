#!/usr/bin/env python3
"""Analyze synthetic personality-institutions data.

This script supports the article "Personality and Institutions: Leadership,
Bureaucracy, and Social Order." It demonstrates institutional-unit summaries,
role-fit metrics, risk metrics, and simple regression-style models using
synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_institutions_bureaucracy.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "conscientiousness",
    "agreeableness",
    "emotional_stability",
    "openness",
    "dark_trait_pressure",
]

OUTCOMES = [
    "leadership_rating",
    "institutional_performance",
    "institutional_trust",
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
        "institutional_unit",
        "role_type",
        *TRAITS,
        "bureaucratic_fit",
        "discretion_level",
        "accountability_strength",
        "role_clarity",
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["role_fit_index"] = (
        df["bureaucratic_fit"]
        + df["conscientiousness"]
        + df["accountability_strength"]
        + df["role_clarity"]
    ) / 4.0

    df["institutional_risk_index"] = (
        df["dark_trait_pressure"]
        + df["discretion_level"]
        - df["accountability_strength"]
        - df["role_clarity"]
    )

    df["stewardship_index"] = (
        df["conscientiousness"]
        + df["agreeableness"]
        + df["emotional_stability"]
        + df["bureaucratic_fit"]
        + df["accountability_strength"]
        - df["dark_trait_pressure"]
    ) / 5.0

    unit_summary = (
        df.groupby("institutional_unit")
        .agg(
            n=("participant_id", "count"),
            role_fit_mean=("role_fit_index", "mean"),
            risk_mean=("institutional_risk_index", "mean"),
            stewardship_mean=("stewardship_index", "mean"),
            performance_mean=("institutional_performance", "mean"),
            trust_mean=("institutional_trust", "mean"),
        )
        .reset_index()
    )

    role_summary = (
        df.groupby("role_type")
        .agg(
            n=("participant_id", "count"),
            discretion_mean=("discretion_level", "mean"),
            accountability_mean=("accountability_strength", "mean"),
            leadership_mean=("leadership_rating", "mean"),
            performance_mean=("institutional_performance", "mean"),
            trust_mean=("institutional_trust", "mean"),
            risk_mean=("institutional_risk_index", "mean"),
        )
        .reset_index()
    )

    unit_summary.to_csv(OUTPUTS / "python_institutional_unit_summary.csv", index=False)
    role_summary.to_csv(OUTPUTS / "python_role_type_summary.csv", index=False)

    corr_cols = TRAITS + [
        "bureaucratic_fit",
        "discretion_level",
        "accountability_strength",
        "role_clarity",
        "role_fit_index",
        "institutional_risk_index",
        "stewardship_index",
    ] + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_trait_institution_correlations.csv")

    model_inputs = [
        "conscientiousness",
        "agreeableness",
        "emotional_stability",
        "openness",
        "dark_trait_pressure",
        "bureaucratic_fit",
        "discretion_level",
        "accountability_strength",
        "role_clarity",
    ]

    models = {
        "leadership_rating": fit_ols(df, "leadership_rating", model_inputs),
        "institutional_performance": fit_ols(df, "institutional_performance", model_inputs),
        "institutional_trust": fit_ols(df, "institutional_trust", model_inputs),
        "note": "Synthetic demonstration only; not a personnel-assessment model.",
    }

    with open(OUTPUTS / "python_institutional_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_personality_institutions.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
