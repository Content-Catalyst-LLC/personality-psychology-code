#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_selfhood_agency_identity.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

BASE = [
    "past_self",
    "present_self",
    "future_self",
    "intentional_clarity",
    "action_ownership",
    "self_efficacy",
    "external_constraint",
    "social_recognition",
    "value_commitment_gap",
    "identity_integration",
    "well_being",
]
DERIVED = [
    "past_present_gap",
    "present_future_gap",
    "temporal_self_continuity",
    "agency_index",
    "situated_agency_index",
    "identity_alignment",
]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "identity_context", *BASE, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["continuity_level"] = np.where(
    df["temporal_self_continuity"] > df["temporal_self_continuity"].median(),
    "higher_continuity",
    "lower_continuity",
)
df["agency_level"] = np.where(
    df["situated_agency_index"] > df["situated_agency_index"].median(),
    "higher_agency",
    "lower_agency",
)
df["identity_profile"] = df["continuity_level"] + "_" + df["agency_level"]
df["high_constraint_low_agency"] = (
    (df["external_constraint"] > df["external_constraint"].median())
    & (df["situated_agency_index"] < df["situated_agency_index"].median())
)
df["low_continuity_low_integration"] = (
    (df["temporal_self_continuity"] < df["temporal_self_continuity"].median())
    & (df["identity_integration"] < df["identity_integration"].median())
)

context_summary = (
    df.groupby("identity_context")
    .agg(
        n=("person_id", "count"),
        temporal_self_continuity_mean=("temporal_self_continuity", "mean"),
        agency_index_mean=("agency_index", "mean"),
        situated_agency_mean=("situated_agency_index", "mean"),
        social_recognition_mean=("social_recognition", "mean"),
        external_constraint_mean=("external_constraint", "mean"),
        identity_integration_mean=("identity_integration", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("identity_profile")
    .agg(
        n=("person_id", "count"),
        temporal_self_continuity_mean=("temporal_self_continuity", "mean"),
        situated_agency_mean=("situated_agency_index", "mean"),
        social_recognition_mean=("social_recognition", "mean"),
        external_constraint_mean=("external_constraint", "mean"),
        identity_integration_mean=("identity_integration", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

disjunction_summary = pd.DataFrame(
    {
        "pattern": ["high_constraint_low_agency", "low_continuity_low_integration"],
        "n": [int(df["high_constraint_low_agency"].sum()), int(df["low_continuity_low_integration"].sum())],
        "proportion": [float(df["high_constraint_low_agency"].mean()), float(df["low_continuity_low_integration"].mean())],
    }
)

corr_cols = BASE + DERIVED
models = {
    "identity_integration": ols(df, "identity_integration", ["temporal_self_continuity", "situated_agency_index", "social_recognition", "external_constraint", "value_commitment_gap"]),
    "well_being": ols(df, "well_being", ["identity_integration", "situated_agency_index", "temporal_self_continuity", "social_recognition", "external_constraint"]),
    "agency_index": ols(df, "agency_index", ["intentional_clarity", "action_ownership", "self_efficacy", "social_recognition", "external_constraint"]),
    "note": "Synthetic demonstration only; not clinical assessment, identity evaluation, personality testing, workplace screening, legal evaluation, or individual prediction.",
}

context_summary.to_csv(OUT / "python_identity_context_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_identity_profile_summary.csv", index=False)
disjunction_summary.to_csv(OUT / "python_identity_disjunction_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_selfhood_agency_identity_correlations.csv")
(OUT / "python_selfhood_agency_identity_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_selfhood_agency_identity.csv", index=False)
print(f"Wrote outputs to {OUT}")
