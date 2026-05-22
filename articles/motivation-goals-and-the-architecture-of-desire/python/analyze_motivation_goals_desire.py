#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_motivation_goals_desire.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

GOALS = [
    "autonomy_goal",
    "achievement_goal",
    "belonging_goal",
    "security_goal",
    "meaning_goal",
    "status_goal",
]
SUPPORT = ["autonomy_support", "competence_support", "relatedness_support"]
REGULATION = ["goal_conflict", "goal_ownership", "conscientiousness", "persistence_score", "adaptive_disengagement"]
DERIVED = [
    "total_goal_intensity",
    "approach_orientation",
    "avoidance_security_orientation",
    "status_orientation",
    "need_support",
    "motivational_quality",
    "life_direction_coherence",
]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "motivation_context", "well_being", *GOALS, *SUPPORT, *REGULATION, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["ownership_level"] = np.where(df["goal_ownership"] > df["goal_ownership"].median(), "higher_ownership", "lower_ownership")
df["conflict_level"] = np.where(df["goal_conflict"] > df["goal_conflict"].median(), "higher_conflict", "lower_conflict")
df["meaning_level"] = np.where(df["meaning_goal"] > df["meaning_goal"].median(), "higher_meaning", "lower_meaning")
df["motivational_profile"] = df["ownership_level"] + "_" + df["conflict_level"] + "_" + df["meaning_level"]

df["high_conflict_low_ownership"] = (
    (df["goal_conflict"] > df["goal_conflict"].median())
    & (df["goal_ownership"] < df["goal_ownership"].median())
)
df["high_status_low_meaning"] = (
    (df["status_goal"] > df["status_goal"].median())
    & (df["meaning_goal"] < df["meaning_goal"].median())
)

context_summary = (
    df.groupby("motivation_context")
    .agg(
        n=("person_id", "count"),
        approach_orientation_mean=("approach_orientation", "mean"),
        status_orientation_mean=("status_orientation", "mean"),
        avoidance_security_orientation_mean=("avoidance_security_orientation", "mean"),
        need_support_mean=("need_support", "mean"),
        goal_ownership_mean=("goal_ownership", "mean"),
        motivational_quality_mean=("motivational_quality", "mean"),
        goal_conflict_mean=("goal_conflict", "mean"),
        persistence_score_mean=("persistence_score", "mean"),
        adaptive_disengagement_mean=("adaptive_disengagement", "mean"),
        life_direction_coherence_mean=("life_direction_coherence", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("motivational_profile")
    .agg(
        n=("person_id", "count"),
        goal_ownership_mean=("goal_ownership", "mean"),
        goal_conflict_mean=("goal_conflict", "mean"),
        meaning_goal_mean=("meaning_goal", "mean"),
        need_support_mean=("need_support", "mean"),
        motivational_quality_mean=("motivational_quality", "mean"),
        life_direction_coherence_mean=("life_direction_coherence", "mean"),
        persistence_score_mean=("persistence_score", "mean"),
        adaptive_disengagement_mean=("adaptive_disengagement", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

pattern_summary = pd.DataFrame({
    "pattern": ["high_conflict_low_ownership", "high_status_low_meaning"],
    "n": [int(df["high_conflict_low_ownership"].sum()), int(df["high_status_low_meaning"].sum())],
    "proportion": [float(df["high_conflict_low_ownership"].mean()), float(df["high_status_low_meaning"].mean())],
})

models = {
    "persistence_score": ols(
        df,
        "persistence_score",
        [
            "autonomy_goal",
            "achievement_goal",
            "belonging_goal",
            "security_goal",
            "meaning_goal",
            "status_goal",
            "goal_conflict",
            "goal_ownership",
            "conscientiousness",
        ],
    ),
    "well_being": ols(
        df,
        "well_being",
        [
            "motivational_quality",
            "life_direction_coherence",
            "goal_conflict",
            "adaptive_disengagement",
            "conscientiousness",
        ],
    ),
    "adaptive_disengagement": ols(
        df,
        "adaptive_disengagement",
        ["goal_conflict", "goal_ownership", "motivational_quality", "conscientiousness"],
    ),
    "life_direction_coherence": ols(
        df,
        "life_direction_coherence",
        ["goal_ownership", "motivational_quality", "approach_orientation", "goal_conflict", "need_support"],
    ),
    "note": "Synthetic demonstration only; not moral ranking, clinical assessment, personality testing, workplace screening, legal evaluation, or individual prediction.",
}

corr_cols = GOALS + SUPPORT + REGULATION + DERIVED + ["well_being"]

context_summary.to_csv(OUT / "python_motivation_context_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_motivation_profile_summary.csv", index=False)
pattern_summary.to_csv(OUT / "python_motivation_pattern_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_motivation_goals_correlations.csv")
(OUT / "python_motivation_goals_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_motivation_goals_desire.csv", index=False)
print(f"Wrote outputs to {OUT}")
