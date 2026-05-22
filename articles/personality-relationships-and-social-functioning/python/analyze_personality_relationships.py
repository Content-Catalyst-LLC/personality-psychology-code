#!/usr/bin/env python3
"""Analyze synthetic personality, relationships, and social functioning data.

This script supports the article "Personality, Relationships, and Social
Functioning." It demonstrates context summaries, domain summaries, trait
correlations, relationship / social functioning models, and relational stability
indices using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_relationships_social_functioning.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
]

CAPACITIES = [
    "empathy",
    "self_regulation",
    "attachment_security",
    "perceived_support",
]

OUTCOMES = [
    "relationship_satisfaction",
    "social_functioning",
    "loneliness",
    "conflict_frequency",
    "reciprocity_quality",
    "reputation_trust",
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
        "social_context",
        "relationship_domain",
        *TRAITS,
        *CAPACITIES,
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["relational_stability_index"] = (
        df["agreeableness"]
        + df["conscientiousness"]
        + df["empathy"]
        + df["self_regulation"]
        + df["attachment_security"]
        - df["neuroticism"]
    ) / 5.0

    df["social_support_index"] = (
        df["perceived_support"]
        + df["relationship_satisfaction"]
        + df["social_functioning"]
        - df["loneliness"]
    ) / 3.0

    df["conflict_risk_index"] = (
        df["neuroticism"]
        + df["conflict_frequency"]
        - df["agreeableness"]
        - df["self_regulation"]
    )

    context_summary = (
        df.groupby("social_context")
        .agg(
            n=("participant_id", "count"),
            relationship_satisfaction_mean=("relationship_satisfaction", "mean"),
            social_functioning_mean=("social_functioning", "mean"),
            loneliness_mean=("loneliness", "mean"),
            conflict_frequency_mean=("conflict_frequency", "mean"),
            perceived_support_mean=("perceived_support", "mean"),
            relational_stability_mean=("relational_stability_index", "mean"),
        )
        .reset_index()
    )

    domain_summary = (
        df.groupby("relationship_domain")
        .agg(
            n=("participant_id", "count"),
            reciprocity_mean=("reciprocity_quality", "mean"),
            reputation_trust_mean=("reputation_trust", "mean"),
            satisfaction_mean=("relationship_satisfaction", "mean"),
            conflict_risk_mean=("conflict_risk_index", "mean"),
        )
        .reset_index()
    )

    context_summary.to_csv(OUTPUTS / "python_social_context_summary.csv", index=False)
    domain_summary.to_csv(OUTPUTS / "python_relationship_domain_summary.csv", index=False)

    corr_cols = TRAITS + CAPACITIES + [
        "relational_stability_index",
        "social_support_index",
        "conflict_risk_index",
    ] + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_trait_relationship_correlations.csv")

    relationship_inputs = TRAITS + ["empathy", "self_regulation", "attachment_security"]
    social_inputs = TRAITS + ["empathy", "self_regulation", "perceived_support"]
    loneliness_inputs = ["extraversion", "agreeableness", "neuroticism", "attachment_security", "perceived_support"]
    conflict_inputs = ["agreeableness", "neuroticism", "self_regulation", "attachment_security"]

    models = {
        "relationship_satisfaction": fit_ols(df, "relationship_satisfaction", relationship_inputs),
        "social_functioning": fit_ols(df, "social_functioning", social_inputs),
        "loneliness": fit_ols(df, "loneliness", loneliness_inputs),
        "conflict_frequency": fit_ols(df, "conflict_frequency", conflict_inputs),
        "note": "Synthetic demonstration only; not a clinical, diagnostic, or relationship-assessment model.",
    }

    with open(OUTPUTS / "python_relationship_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_personality_relationships.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
