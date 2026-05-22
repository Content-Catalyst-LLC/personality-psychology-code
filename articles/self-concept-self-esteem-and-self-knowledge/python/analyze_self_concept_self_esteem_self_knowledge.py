#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_self_concept_self_esteem_self_knowledge.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

SELF_COLS = ["self_warmth", "self_conscientiousness", "self_emotional_stability", "self_openness"]
OTHER_COLS = ["other_warmth", "other_conscientiousness", "other_emotional_stability", "other_openness"]
BASE = SELF_COLS + OTHER_COLS + [
    "actual_self",
    "ideal_self",
    "ought_self",
    "self_esteem",
    "social_recognition",
    "external_devaluation",
    "well_being",
]
DERIVED = [
    "warmth_gap",
    "conscientiousness_gap",
    "emotional_stability_gap",
    "openness_gap",
    "self_other_gap_mean",
    "self_knowledge_accuracy",
    "actual_ideal_discrepancy",
    "actual_ought_discrepancy",
    "total_self_discrepancy",
    "self_concept_positivity",
]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "self_system_context", *BASE, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

agreement_summary = pd.DataFrame({
    "domain": ["warmth", "conscientiousness", "emotional_stability", "openness"],
    "self_other_agreement": [
        df["self_warmth"].corr(df["other_warmth"]),
        df["self_conscientiousness"].corr(df["other_conscientiousness"]),
        df["self_emotional_stability"].corr(df["other_emotional_stability"]),
        df["self_openness"].corr(df["other_openness"]),
    ],
})

df["esteem_level"] = np.where(df["self_esteem"] > df["self_esteem"].median(), "higher_self_esteem", "lower_self_esteem")
df["accuracy_level"] = np.where(df["self_knowledge_accuracy"] > df["self_knowledge_accuracy"].median(), "higher_self_knowledge", "lower_self_knowledge")
df["discrepancy_level"] = np.where(df["total_self_discrepancy"] > df["total_self_discrepancy"].median(), "higher_discrepancy", "lower_discrepancy")
df["self_system_profile"] = df["esteem_level"] + "_" + df["accuracy_level"] + "_" + df["discrepancy_level"]

df["high_esteem_low_accuracy"] = (
    (df["self_esteem"] > df["self_esteem"].median())
    & (df["self_knowledge_accuracy"] < df["self_knowledge_accuracy"].median())
)
df["low_esteem_high_devaluation"] = (
    (df["self_esteem"] < df["self_esteem"].median())
    & (df["external_devaluation"] > df["external_devaluation"].median())
)

context_summary = (
    df.groupby("self_system_context")
    .agg(
        n=("person_id", "count"),
        self_concept_positivity_mean=("self_concept_positivity", "mean"),
        self_esteem_mean=("self_esteem", "mean"),
        self_knowledge_accuracy_mean=("self_knowledge_accuracy", "mean"),
        total_self_discrepancy_mean=("total_self_discrepancy", "mean"),
        social_recognition_mean=("social_recognition", "mean"),
        external_devaluation_mean=("external_devaluation", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("self_system_profile")
    .agg(
        n=("person_id", "count"),
        self_esteem_mean=("self_esteem", "mean"),
        self_knowledge_accuracy_mean=("self_knowledge_accuracy", "mean"),
        total_self_discrepancy_mean=("total_self_discrepancy", "mean"),
        social_recognition_mean=("social_recognition", "mean"),
        external_devaluation_mean=("external_devaluation", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

pattern_summary = pd.DataFrame({
    "pattern": ["high_esteem_low_accuracy", "low_esteem_high_devaluation"],
    "n": [int(df["high_esteem_low_accuracy"].sum()), int(df["low_esteem_high_devaluation"].sum())],
    "proportion": [float(df["high_esteem_low_accuracy"].mean()), float(df["low_esteem_high_devaluation"].mean())],
})

models = {
    "self_esteem": ols(df, "self_esteem", ["self_concept_positivity", "total_self_discrepancy", "self_knowledge_accuracy", "social_recognition", "external_devaluation"]),
    "well_being": ols(df, "well_being", ["self_esteem", "total_self_discrepancy", "self_knowledge_accuracy", "social_recognition", "external_devaluation"]),
    "self_knowledge_accuracy": ols(df, "self_knowledge_accuracy", ["social_recognition", "external_devaluation", "self_concept_positivity", "self_esteem"]),
    "note": "Synthetic demonstration only; not clinical assessment, identity evaluation, personality testing, workplace screening, legal evaluation, or individual prediction.",
}

corr_cols = BASE + DERIVED
context_summary.to_csv(OUT / "python_self_system_context_summary.csv", index=False)
agreement_summary.to_csv(OUT / "python_self_other_agreement_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_self_system_profile_summary.csv", index=False)
pattern_summary.to_csv(OUT / "python_self_system_pattern_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_self_system_correlations.csv")
(OUT / "python_self_system_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_self_concept_self_esteem_self_knowledge.csv", index=False)
print(f"Wrote outputs to {OUT}")
