#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_traits_character_morality.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAITS = ["honesty_humility", "conscientiousness", "agreeableness", "emotional_stability", "openness"]
LAYERS = ["moral_identity", "practical_judgment", "institutional_accountability", "power_pressure", "social_desirability_pressure"]
OUTCOMES = ["ethical_behavior", "integrity_rating", "trustworthiness_rating"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"participant_id", "evaluation_context", *TRAITS, *LAYERS, *OUTCOMES}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["descriptive_trait_reliability"] = df[["honesty_humility", "conscientiousness", "agreeableness"]].mean(axis=1)
df["moral_character_index"] = df[OUTCOMES].mean(axis=1)
df["judgment_context_index"] = df[["practical_judgment", "institutional_accountability"]].mean(axis=1)
df["trait_character_gap"] = df["moral_character_index"] - df["descriptive_trait_reliability"]
df["trait_reliability_level"] = np.where(df["descriptive_trait_reliability"] > df["descriptive_trait_reliability"].median(), "higher_trait_reliability", "lower_trait_reliability")
df["character_level"] = np.where(df["moral_character_index"] > df["moral_character_index"].median(), "higher_character_evaluation", "lower_character_evaluation")
df["trait_character_profile"] = df["trait_reliability_level"] + "_" + df["character_level"]
df["gap_direction"] = np.where(df["trait_character_gap"] >= 0, "character_evaluation_exceeds_trait_reliability", "trait_reliability_exceeds_character_evaluation")

df.groupby("evaluation_context").agg(
    n=("participant_id", "count"),
    trait_reliability_mean=("descriptive_trait_reliability", "mean"),
    moral_character_mean=("moral_character_index", "mean"),
    moral_identity_mean=("moral_identity", "mean"),
    practical_judgment_mean=("practical_judgment", "mean"),
    accountability_mean=("institutional_accountability", "mean"),
    power_pressure_mean=("power_pressure", "mean"),
).reset_index().to_csv(OUT / "python_evaluation_context_summary.csv", index=False)

df.groupby("trait_character_profile").agg(
    n=("participant_id", "count"),
    trait_reliability_mean=("descriptive_trait_reliability", "mean"),
    moral_character_mean=("moral_character_index", "mean"),
    moral_identity_mean=("moral_identity", "mean"),
    practical_judgment_mean=("practical_judgment", "mean"),
    accountability_mean=("institutional_accountability", "mean"),
).reset_index().to_csv(OUT / "python_trait_character_profile_summary.csv", index=False)

df.groupby("gap_direction").agg(
    n=("participant_id", "count"),
    trait_reliability_mean=("descriptive_trait_reliability", "mean"),
    moral_character_mean=("moral_character_index", "mean"),
    practical_judgment_mean=("practical_judgment", "mean"),
    power_pressure_mean=("power_pressure", "mean"),
).reset_index().to_csv(OUT / "python_trait_character_gap_summary.csv", index=False)

corr_cols = TRAITS + LAYERS + OUTCOMES + ["descriptive_trait_reliability", "moral_character_index", "judgment_context_index", "trait_character_gap"]
df[corr_cols].corr().to_csv(OUT / "python_traits_character_correlations.csv")

models = {
    "ethical_behavior": ols(df, "ethical_behavior", TRAITS + ["moral_identity"]),
    "moral_character_index": ols(df, "moral_character_index", ["descriptive_trait_reliability", "moral_identity", "practical_judgment", "institutional_accountability"]),
    "trait_character_gap": ols(df, "trait_character_gap", ["moral_identity", "practical_judgment", "institutional_accountability", "power_pressure", "social_desirability_pressure"]),
    "note": "Synthetic demonstration only; not moral ranking, hiring guidance, legal evaluation, or social sorting."
}
(OUT / "python_traits_character_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_traits_character_morality.csv", index=False)
print(f"Wrote outputs to {OUT}")
