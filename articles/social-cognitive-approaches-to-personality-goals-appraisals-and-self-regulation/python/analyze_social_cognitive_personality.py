#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_social_cognitive_personality.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

PROCESSES = [
    "goal_activation",
    "threat_appraisal",
    "challenge_appraisal",
    "self_efficacy",
    "self_regulation",
    "emotional_arousal",
    "perceived_support",
]
OUTCOMES = ["prosocial_behavior", "avoidance_behavior", "task_persistence"]
DERIVED = ["appraisal_balance", "regulation_capacity", "approach_orientation", "avoidance_pressure"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "occasion", "situation_type", *PROCESSES, *OUTCOMES, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

person_summary = (
    df.groupby("person_id")
    .agg(
        n_occasions=("occasion", "count"),
        goal_activation_mean=("goal_activation", "mean"),
        threat_appraisal_mean=("threat_appraisal", "mean"),
        challenge_appraisal_mean=("challenge_appraisal", "mean"),
        self_efficacy_mean=("self_efficacy", "mean"),
        self_regulation_mean=("self_regulation", "mean"),
        prosocial_behavior_mean=("prosocial_behavior", "mean"),
        avoidance_behavior_mean=("avoidance_behavior", "mean"),
        task_persistence_mean=("task_persistence", "mean"),
    )
    .reset_index()
)

situation_summary = (
    df.groupby("situation_type")
    .agg(
        n=("situation_type", "count"),
        goal_activation_mean=("goal_activation", "mean"),
        threat_appraisal_mean=("threat_appraisal", "mean"),
        challenge_appraisal_mean=("challenge_appraisal", "mean"),
        self_efficacy_mean=("self_efficacy", "mean"),
        self_regulation_mean=("self_regulation", "mean"),
        emotional_arousal_mean=("emotional_arousal", "mean"),
        perceived_support_mean=("perceived_support", "mean"),
        prosocial_behavior_mean=("prosocial_behavior", "mean"),
        avoidance_behavior_mean=("avoidance_behavior", "mean"),
        task_persistence_mean=("task_persistence", "mean"),
    )
    .reset_index()
)

if_then_summary = (
    df.groupby("situation_type")
    .agg(
        threat_appraisal_mean=("threat_appraisal", "mean"),
        challenge_appraisal_mean=("challenge_appraisal", "mean"),
        prosocial_behavior_mean=("prosocial_behavior", "mean"),
        avoidance_behavior_mean=("avoidance_behavior", "mean"),
        task_persistence_mean=("task_persistence", "mean"),
    )
    .reset_index()
)

person_summary.to_csv(OUT / "python_person_summary.csv", index=False)
situation_summary.to_csv(OUT / "python_situation_summary.csv", index=False)
if_then_summary.to_csv(OUT / "python_if_then_summary.csv", index=False)

corr_cols = PROCESSES + DERIVED + OUTCOMES
df[corr_cols].corr().to_csv(OUT / "python_social_cognitive_correlations.csv")

predictors = [
    "goal_activation",
    "threat_appraisal",
    "challenge_appraisal",
    "self_efficacy",
    "self_regulation",
    "emotional_arousal",
    "perceived_support",
]
models = {
    "prosocial_behavior": ols(df, "prosocial_behavior", predictors),
    "avoidance_behavior": ols(df, "avoidance_behavior", predictors),
    "task_persistence": ols(df, "task_persistence", predictors),
    "note": "Synthetic demonstration only; not personality testing, clinical assessment, educational placement, workplace screening, or individual ranking.",
}

(OUT / "python_social_cognitive_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_social_cognitive_personality.csv", index=False)
print(f"Wrote outputs to {OUT}")
