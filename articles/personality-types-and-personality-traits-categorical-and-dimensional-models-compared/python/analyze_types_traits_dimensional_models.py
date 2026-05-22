#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_types_traits_dimensional_models.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAITS = ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]
REQUIRED = {
    "person_id",
    "assessment_context",
    *TRAITS,
    "extraversion_category",
    "conscientiousness_category",
    "neuroticism_category",
    "profile_type",
    "synthetic_cluster",
    "nearest_threshold_distance",
    "near_threshold_boundary",
    "cluster_boundary_margin",
    "near_cluster_boundary",
    "dimensional_signal_strength",
    "information_loss_index",
    "well_being",
    "collaboration_score",
    "reflective_utility_score",
}

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((df[y].to_numpy(float) - pred) ** 2))
    ss_tot = float(np.sum((df[y].to_numpy(float) - df[y].mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot
    return {
        "coefficients": dict(zip(["intercept", *xs], map(float, beta))),
        "r_squared": r2,
    }

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

context_summary = (
    df.groupby("assessment_context")
    .agg(
        n=("person_id", "count"),
        near_threshold_rate=("near_threshold_boundary", "mean"),
        near_cluster_boundary_rate=("near_cluster_boundary", "mean"),
        information_loss_mean=("information_loss_index", "mean"),
        dimensional_signal_mean=("dimensional_signal_strength", "mean"),
        well_being_mean=("well_being", "mean"),
        collaboration_score_mean=("collaboration_score", "mean"),
        reflective_utility_mean=("reflective_utility_score", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("profile_type")
    .agg(
        n=("person_id", "count"),
        extraversion_mean=("extraversion", "mean"),
        agreeableness_mean=("agreeableness", "mean"),
        conscientiousness_mean=("conscientiousness", "mean"),
        neuroticism_mean=("neuroticism", "mean"),
        openness_mean=("openness", "mean"),
        well_being_mean=("well_being", "mean"),
        collaboration_score_mean=("collaboration_score", "mean"),
        information_loss_mean=("information_loss_index", "mean"),
    )
    .reset_index()
)

cluster_summary = (
    df.groupby("synthetic_cluster")
    .agg(
        n=("person_id", "count"),
        extraversion_mean=("extraversion", "mean"),
        agreeableness_mean=("agreeableness", "mean"),
        conscientiousness_mean=("conscientiousness", "mean"),
        neuroticism_mean=("neuroticism", "mean"),
        openness_mean=("openness", "mean"),
        near_cluster_boundary_rate=("near_cluster_boundary", "mean"),
        well_being_mean=("well_being", "mean"),
        collaboration_score_mean=("collaboration_score", "mean"),
    )
    .reset_index()
)

boundary_cases = (
    df[(df["near_threshold_boundary"] == 1) | (df["near_cluster_boundary"] == 1)]
    .sort_values(["nearest_threshold_distance", "cluster_boundary_margin"])
    .loc[
        :,
        [
            "person_id",
            "assessment_context",
            "profile_type",
            "synthetic_cluster",
            "extraversion",
            "agreeableness",
            "conscientiousness",
            "neuroticism",
            "openness",
            "nearest_threshold_distance",
            "near_threshold_boundary",
            "cluster_boundary_margin",
            "near_cluster_boundary",
            "information_loss_index",
        ],
    ]
)

# Continuous models preserve dimensional signal.
models = {
    "well_being_continuous_traits": ols(df, "well_being", TRAITS),
    "collaboration_continuous_traits": ols(df, "collaboration_score", TRAITS),
    "reflective_utility_continuous_plus_loss": ols(
        df,
        "reflective_utility_score",
        TRAITS + ["information_loss_index", "near_threshold_boundary", "near_cluster_boundary"],
    ),
    "note": "Categorical profile and cluster summaries can support interpretation, but dimensional trait scores usually preserve more information.",
    "professional_use_boundary": "Suitable for education, research prototyping, consulting support, organizational learning, and methodological demonstration; not a standalone assessment or decision system for consequential individual decisions.",
}

type_counts = df["profile_type"].value_counts().rename_axis("profile_type").reset_index(name="n")
type_counts["proportion"] = type_counts["n"] / len(df)

category_crosswalk = (
    df.groupby(["extraversion_category", "conscientiousness_category", "neuroticism_category", "profile_type"])
    .size()
    .reset_index(name="n")
    .sort_values("n", ascending=False)
)

corr_cols = TRAITS + [
    "nearest_threshold_distance",
    "near_threshold_boundary",
    "cluster_boundary_margin",
    "near_cluster_boundary",
    "dimensional_signal_strength",
    "information_loss_index",
    "well_being",
    "collaboration_score",
    "reflective_utility_score",
]

context_summary.to_csv(OUT / "python_context_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_profile_type_summary.csv", index=False)
cluster_summary.to_csv(OUT / "python_cluster_summary.csv", index=False)
boundary_cases.to_csv(OUT / "python_boundary_cases.csv", index=False)
type_counts.to_csv(OUT / "python_profile_type_counts.csv", index=False)
category_crosswalk.to_csv(OUT / "python_category_crosswalk.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_dimensional_correlations.csv")
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_types_traits_dimensional_models.csv", index=False)
print(f"Wrote outputs to {OUT}")
