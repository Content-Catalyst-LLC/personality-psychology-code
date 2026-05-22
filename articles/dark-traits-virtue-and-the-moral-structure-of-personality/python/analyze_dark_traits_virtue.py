#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_dark_traits_virtue_personality.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

DARK = ["machiavellianism", "narcissism", "psychopathy", "sadism"]
VIRTUE = ["honesty_humility", "conscientious_reliability", "fairness_orientation", "compassion_kindness"]
LAYERS = ["moral_identity", "practical_judgment", "institutional_accountability", "status_reward_pressure"]
OUTCOMES = ["unethical_behavior", "prosocial_restraint", "harm_indicator"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"participant_id", "institutional_context", *DARK, *VIRTUE, *LAYERS, *OUTCOMES}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["dark_trait_burden"] = df[DARK].mean(axis=1)
df["virtue_relevant_tendency"] = df[VIRTUE].mean(axis=1)
df["moral_integration_index"] = (df["virtue_relevant_tendency"] + df["moral_identity"] + df["practical_judgment"]) / 3
df["dark_accountability_risk"] = df["dark_trait_burden"] * (7 - df["institutional_accountability"])
df["dominant_dark_trait"] = df[DARK].idxmax(axis=1)
df["dark_level"] = np.where(df["dark_trait_burden"] > df["dark_trait_burden"].median(), "higher_darkness", "lower_darkness")
df["virtue_level"] = np.where(df["virtue_relevant_tendency"] > df["virtue_relevant_tendency"].median(), "higher_virtue_relevant", "lower_virtue_relevant")
df["moral_profile"] = df["dark_level"] + "_" + df["virtue_level"]

df.groupby("institutional_context").agg(
    n=("participant_id", "count"),
    dark_trait_burden_mean=("dark_trait_burden", "mean"),
    virtue_relevant_mean=("virtue_relevant_tendency", "mean"),
    accountability_mean=("institutional_accountability", "mean"),
    status_pressure_mean=("status_reward_pressure", "mean"),
    unethical_behavior_mean=("unethical_behavior", "mean"),
    prosocial_restraint_mean=("prosocial_restraint", "mean"),
    harm_indicator_mean=("harm_indicator", "mean"),
).reset_index().to_csv(OUT / "python_institutional_context_summary.csv", index=False)

df.groupby("moral_profile").agg(
    n=("participant_id", "count"),
    dark_trait_burden_mean=("dark_trait_burden", "mean"),
    virtue_relevant_mean=("virtue_relevant_tendency", "mean"),
    moral_integration_mean=("moral_integration_index", "mean"),
    unethical_behavior_mean=("unethical_behavior", "mean"),
    prosocial_restraint_mean=("prosocial_restraint", "mean"),
    harm_indicator_mean=("harm_indicator", "mean"),
).reset_index().to_csv(OUT / "python_moral_profile_summary.csv", index=False)

df.groupby("dominant_dark_trait").agg(
    n=("participant_id", "count"),
    dark_trait_burden_mean=("dark_trait_burden", "mean"),
    unethical_behavior_mean=("unethical_behavior", "mean"),
    harm_indicator_mean=("harm_indicator", "mean"),
    virtue_relevant_mean=("virtue_relevant_tendency", "mean"),
).reset_index().to_csv(OUT / "python_dominant_dark_trait_summary.csv", index=False)

corr_cols = DARK + VIRTUE + LAYERS + OUTCOMES + ["dark_trait_burden", "virtue_relevant_tendency", "moral_integration_index", "dark_accountability_risk"]
df[corr_cols].corr().to_csv(OUT / "python_dark_traits_virtue_correlations.csv")

models = {
    "unethical_behavior": ols(df, "unethical_behavior", DARK + VIRTUE),
    "prosocial_restraint": ols(df, "prosocial_restraint", ["dark_trait_burden", "virtue_relevant_tendency", "moral_identity", "practical_judgment"]),
    "harm_indicator": ols(df, "harm_indicator", ["dark_trait_burden", "virtue_relevant_tendency", "institutional_accountability", "status_reward_pressure", "dark_accountability_risk"]),
    "note": "Synthetic demonstration only; not moral ranking, hiring guidance, legal evaluation, or social sorting."
}
(OUT / "python_dark_traits_virtue_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_dark_traits_virtue.csv", index=False)
print(f"Wrote outputs to {OUT}")
