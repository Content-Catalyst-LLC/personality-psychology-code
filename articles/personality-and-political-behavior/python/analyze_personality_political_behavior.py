#!/usr/bin/env python3
"""Analyze synthetic personality and political behavior data.

This script supports the article "Personality and Political Behavior." It
demonstrates context summaries, trait correlations, participation pathways,
identity-threat metrics, and simple regression-style models using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_political_behavior.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
]

OUTCOMES = [
    "ideology_score",
    "political_participation",
    "affective_polarization",
    "trust_in_institutions",
    "leadership_authority_preference",
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
        "country_context",
        "political_system_type",
        *TRAITS,
        "political_interest",
        "political_efficacy",
        "group_identity_strength",
        "perceived_threat",
        "media_exposure",
        "civic_opportunity",
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["engagement_capacity"] = (
        df["extraversion"]
        + df["political_interest"]
        + df["political_efficacy"]
        + df["civic_opportunity"]
    ) / 4.0

    df["identity_threat_index"] = (
        df["group_identity_strength"]
        + df["perceived_threat"]
        + df["media_exposure"]
    ) / 3.0

    df["pluralism_openness_index"] = (
        df["openness"]
        + df["agreeableness"]
        + df["trust_in_institutions"]
        - df["affective_polarization"]
    ) / 3.0

    context_summary = (
        df.groupby("country_context")
        .agg(
            n=("participant_id", "count"),
            ideology_mean=("ideology_score", "mean"),
            participation_mean=("political_participation", "mean"),
            polarization_mean=("affective_polarization", "mean"),
            institutional_trust_mean=("trust_in_institutions", "mean"),
            leadership_authority_preference_mean=("leadership_authority_preference", "mean"),
            engagement_capacity_mean=("engagement_capacity", "mean"),
            identity_threat_mean=("identity_threat_index", "mean"),
        )
        .reset_index()
    )

    system_summary = (
        df.groupby("political_system_type")
        .agg(
            n=("participant_id", "count"),
            political_interest_mean=("political_interest", "mean"),
            political_efficacy_mean=("political_efficacy", "mean"),
            civic_opportunity_mean=("civic_opportunity", "mean"),
            participation_mean=("political_participation", "mean"),
            trust_mean=("trust_in_institutions", "mean"),
        )
        .reset_index()
    )

    context_summary.to_csv(OUTPUTS / "python_context_summary.csv", index=False)
    system_summary.to_csv(OUTPUTS / "python_system_summary.csv", index=False)

    corr_cols = TRAITS + [
        "political_interest",
        "political_efficacy",
        "group_identity_strength",
        "perceived_threat",
        "media_exposure",
        "civic_opportunity",
        "engagement_capacity",
        "identity_threat_index",
        "pluralism_openness_index",
    ] + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_trait_politics_correlations.csv")

    ideology_inputs = TRAITS + ["group_identity_strength", "perceived_threat", "trust_in_institutions"]
    participation_inputs = TRAITS + ["political_interest", "political_efficacy", "civic_opportunity"]
    polarization_inputs = ["group_identity_strength", "perceived_threat", "media_exposure", "neuroticism", "agreeableness"]
    authority_inputs = ["conscientiousness", "neuroticism", "perceived_threat", "trust_in_institutions", "openness"]

    models = {
        "ideology_score": fit_ols(df, "ideology_score", ideology_inputs),
        "political_participation": fit_ols(df, "political_participation", participation_inputs),
        "affective_polarization": fit_ols(df, "affective_polarization", polarization_inputs),
        "leadership_authority_preference": fit_ols(df, "leadership_authority_preference", authority_inputs),
        "note": "Synthetic demonstration only; not a voter-profiling or political-targeting model.",
    }

    with open(OUTPUTS / "python_political_behavior_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_personality_political_behavior.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
