#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_mbti_typology_vs_traits.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

DIMENSIONS = ["observed_ei", "observed_sn", "observed_tf", "observed_jp"]
LATENT = ["latent_ei", "latent_sn", "latent_tf", "latent_jp"]
RETEST = ["retest_ei", "retest_sn", "retest_tf", "retest_jp"]
REQUIRED = {
    "person_id",
    "assessment_context",
    *LATENT,
    *DIMENSIONS,
    *RETEST,
    "ei_letter",
    "sn_letter",
    "tf_letter",
    "jp_letter",
    "type_code",
    "retest_type_code",
    "type_changed_on_retest",
    "min_absolute_distance_to_boundary",
    "near_boundary",
    "continuous_signal_strength",
    "boundary_risk_score",
    "information_loss_index",
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

type_frequencies = df["type_code"].value_counts().rename_axis("type_code").reset_index(name="n")
type_frequencies["proportion"] = type_frequencies["n"] / len(df)

context_summary = (
    df.groupby("assessment_context")
    .agg(
        n=("person_id", "count"),
        near_boundary_rate=("near_boundary", "mean"),
        type_change_rate=("type_changed_on_retest", "mean"),
        boundary_risk_mean=("boundary_risk_score", "mean"),
        information_loss_mean=("information_loss_index", "mean"),
        collaboration_score_mean=("collaboration_score", "mean"),
        reflective_utility_mean=("reflective_utility_score", "mean"),
    )
    .reset_index()
)

within_type_variation = (
    df.groupby("type_code")[DIMENSIONS + ["collaboration_score", "reflective_utility_score"]]
    .agg(["count", "mean", "std", "min", "max"])
)
within_type_variation.columns = ["_".join(col).strip("_") for col in within_type_variation.columns]
within_type_variation = within_type_variation.reset_index()

boundary_cases = (
    df[df["near_boundary"]]
    .sort_values("min_absolute_distance_to_boundary")
    .loc[
        :,
        [
            "person_id",
            "assessment_context",
            "type_code",
            "retest_type_code",
            "type_changed_on_retest",
            "observed_ei",
            "observed_sn",
            "observed_tf",
            "observed_jp",
            "min_absolute_distance_to_boundary",
            "boundary_risk_score",
            "information_loss_index",
        ],
    ]
)

models = {
    "continuous_collaboration": ols(df, "collaboration_score", DIMENSIONS),
    "continuous_reflective_utility": ols(df, "reflective_utility_score", DIMENSIONS + ["boundary_risk_score"]),
    "category_note": "Categorical type-code modeling should be compared against continuous-dimensional models. This script reports type summaries and continuous OLS models to emphasize information retention.",
    "responsible_use": "Synthetic demonstration only; not for hiring, promotion, clinical assessment, educational placement, relationship matching, legal evaluation, or individual prediction.",
}

type_change_summary = pd.DataFrame(
    {
        "metric": [
            "n",
            "near_boundary_n",
            "near_boundary_rate",
            "type_changed_on_retest_n",
            "type_changed_on_retest_rate",
            "mean_information_loss_index",
            "mean_boundary_risk_score",
        ],
        "value": [
            len(df),
            int(df["near_boundary"].sum()),
            float(df["near_boundary"].mean()),
            int(df["type_changed_on_retest"].sum()),
            float(df["type_changed_on_retest"].mean()),
            float(df["information_loss_index"].mean()),
            float(df["boundary_risk_score"].mean()),
        ],
    }
)

corr_cols = LATENT + DIMENSIONS + RETEST + [
    "min_absolute_distance_to_boundary",
    "continuous_signal_strength",
    "boundary_risk_score",
    "information_loss_index",
    "collaboration_score",
    "reflective_utility_score",
]

type_frequencies.to_csv(OUT / "python_mbti_type_frequencies.csv", index=False)
context_summary.to_csv(OUT / "python_mbti_context_summary.csv", index=False)
within_type_variation.to_csv(OUT / "python_mbti_within_type_variation.csv", index=False)
boundary_cases.to_csv(OUT / "python_mbti_boundary_cases.csv", index=False)
type_change_summary.to_csv(OUT / "python_mbti_type_change_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_mbti_dimensional_correlations.csv")
(OUT / "python_mbti_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_mbti_typology_vs_traits.csv", index=False)
print(f"Wrote outputs to {OUT}")
