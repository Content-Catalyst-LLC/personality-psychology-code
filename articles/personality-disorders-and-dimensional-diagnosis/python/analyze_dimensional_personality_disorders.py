#!/usr/bin/env python3
"""Analyze synthetic dimensional personality-disorder data.

This script supports the article "Personality Disorders and Dimensional
Diagnosis." It demonstrates severity-band summaries, trait-domain summaries,
functioning impairment models, risk models, and treatment-engagement models
using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_disorders_dimensional_diagnosis.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "negative_affectivity",
    "detachment",
    "antagonism",
    "disinhibition",
    "psychoticism",
    "anankastia",
]

FUNCTIONING = [
    "identity_impairment",
    "self_direction_impairment",
    "empathy_impairment",
    "intimacy_impairment",
]

OUTCOMES = [
    "pd_severity",
    "risk_level",
    "treatment_engagement",
    "borderline_pattern_indicator",
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
        "clinical_context",
        *TRAITS,
        *FUNCTIONING,
        "self_functioning",
        "interpersonal_functioning",
        "functioning_impairment",
        "maladaptive_trait_burden",
        "severity_trait_interaction",
        "perceived_support",
        *OUTCOMES,
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["dominant_trait_domain"] = df[TRAITS].idxmax(axis=1)

    conditions = [
        df["pd_severity"] < 2.5,
        (df["pd_severity"] >= 2.5) & (df["pd_severity"] < 4.5),
        df["pd_severity"] >= 4.5,
    ]
    choices = ["lower_severity", "moderate_severity", "higher_severity"]
    df["severity_band"] = np.select(conditions, choices, default="unclassified")

    context_summary = (
        df.groupby("clinical_context")
        .agg(
            n=("participant_id", "count"),
            functioning_impairment_mean=("functioning_impairment", "mean"),
            trait_burden_mean=("maladaptive_trait_burden", "mean"),
            pd_severity_mean=("pd_severity", "mean"),
            risk_level_mean=("risk_level", "mean"),
            treatment_engagement_mean=("treatment_engagement", "mean"),
            perceived_support_mean=("perceived_support", "mean"),
        )
        .reset_index()
    )

    severity_summary = (
        df.groupby("severity_band")
        .agg(
            n=("participant_id", "count"),
            functioning_impairment_mean=("functioning_impairment", "mean"),
            trait_burden_mean=("maladaptive_trait_burden", "mean"),
            negative_affectivity_mean=("negative_affectivity", "mean"),
            detachment_mean=("detachment", "mean"),
            antagonism_mean=("antagonism", "mean"),
            disinhibition_mean=("disinhibition", "mean"),
            psychoticism_mean=("psychoticism", "mean"),
            anankastia_mean=("anankastia", "mean"),
            borderline_pattern_mean=("borderline_pattern_indicator", "mean"),
            risk_level_mean=("risk_level", "mean"),
        )
        .reset_index()
    )

    domain_summary = (
        df.groupby("dominant_trait_domain")
        .agg(
            n=("participant_id", "count"),
            pd_severity_mean=("pd_severity", "mean"),
            functioning_impairment_mean=("functioning_impairment", "mean"),
            risk_level_mean=("risk_level", "mean"),
            treatment_engagement_mean=("treatment_engagement", "mean"),
            perceived_support_mean=("perceived_support", "mean"),
        )
        .reset_index()
    )

    context_summary.to_csv(OUTPUTS / "python_clinical_context_summary.csv", index=False)
    severity_summary.to_csv(OUTPUTS / "python_severity_band_summary.csv", index=False)
    domain_summary.to_csv(OUTPUTS / "python_dominant_trait_domain_summary.csv", index=False)

    corr_cols = TRAITS + FUNCTIONING + [
        "self_functioning",
        "interpersonal_functioning",
        "functioning_impairment",
        "maladaptive_trait_burden",
        "severity_trait_interaction",
        "perceived_support",
    ] + OUTCOMES

    df[corr_cols].corr().to_csv(OUTPUTS / "python_dimensional_pd_correlations.csv")

    severity_inputs = TRAITS + ["functioning_impairment"]
    interaction_inputs = ["functioning_impairment", "maladaptive_trait_burden", "severity_trait_interaction"]
    risk_inputs = ["pd_severity", "negative_affectivity", "disinhibition", "antagonism", "functioning_impairment"]
    treatment_inputs = ["pd_severity", "functioning_impairment", "negative_affectivity", "detachment", "perceived_support"]

    models = {
        "pd_severity": fit_ols(df, "pd_severity", severity_inputs),
        "severity_trait_interaction_model": fit_ols(df, "pd_severity", interaction_inputs),
        "risk_level": fit_ols(df, "risk_level", risk_inputs),
        "treatment_engagement": fit_ols(df, "treatment_engagement", treatment_inputs),
        "note": "Synthetic demonstration only; not a clinical, diagnostic, risk-assessment, or treatment-planning model.",
    }

    with open(OUTPUTS / "python_dimensional_pd_models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    df.to_csv(OUTPUTS / "python_scored_dimensional_personality_disorders.csv", index=False)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
