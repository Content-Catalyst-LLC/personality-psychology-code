#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_psychodynamic_personality.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

DEFENSES = ["mature_defenses", "neurotic_defenses", "immature_defenses", "defensive_rigidity"]
ATTACHMENT = ["attachment_anxiety", "attachment_avoidance"]
SELF_RELATIONAL = ["self_cohesion", "relational_security", "reflective_functioning"]
OUTCOMES = ["character_integration", "symptom_distress"]
DERIVED = ["defensive_maturity", "attachment_insecurity", "self_relational_capacity", "hidden_structure_risk"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "developmental_context", *DEFENSES, *ATTACHMENT, *SELF_RELATIONAL, *OUTCOMES, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

conditions = [
    (df["mature_defenses"] > df["immature_defenses"]) & (df["mature_defenses"] > df["neurotic_defenses"]),
    (df["immature_defenses"] > df["mature_defenses"]) & (df["immature_defenses"] > df["neurotic_defenses"]),
    (df["neurotic_defenses"] > df["mature_defenses"]) & (df["neurotic_defenses"] > df["immature_defenses"]),
]
choices = ["mature_defense_dominant", "immature_defense_dominant", "neurotic_defense_dominant"]
df["defense_profile"] = np.select(conditions, choices, default="mixed_defensive_profile")

df["integration_band"] = pd.qcut(
    df["character_integration"],
    q=4,
    labels=["lowest_integration", "lower_mid_integration", "upper_mid_integration", "highest_integration"],
)

context_summary = (
    df.groupby("developmental_context")
    .agg(
        n=("person_id", "count"),
        mature_defenses_mean=("mature_defenses", "mean"),
        immature_defenses_mean=("immature_defenses", "mean"),
        defensive_rigidity_mean=("defensive_rigidity", "mean"),
        attachment_insecurity_mean=("attachment_insecurity", "mean"),
        self_relational_capacity_mean=("self_relational_capacity", "mean"),
        character_integration_mean=("character_integration", "mean"),
        symptom_distress_mean=("symptom_distress", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("defense_profile")
    .agg(
        n=("person_id", "count"),
        defensive_maturity_mean=("defensive_maturity", "mean"),
        attachment_insecurity_mean=("attachment_insecurity", "mean"),
        self_relational_capacity_mean=("self_relational_capacity", "mean"),
        character_integration_mean=("character_integration", "mean"),
        symptom_distress_mean=("symptom_distress", "mean"),
    )
    .reset_index()
)

integration_summary = (
    df.groupby("integration_band", observed=True)
    .agg(
        n=("person_id", "count"),
        defensive_maturity_mean=("defensive_maturity", "mean"),
        attachment_insecurity_mean=("attachment_insecurity", "mean"),
        self_relational_capacity_mean=("self_relational_capacity", "mean"),
        hidden_structure_risk_mean=("hidden_structure_risk", "mean"),
        symptom_distress_mean=("symptom_distress", "mean"),
    )
    .reset_index()
)

context_summary.to_csv(OUT / "python_developmental_context_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_defense_profile_summary.csv", index=False)
integration_summary.to_csv(OUT / "python_integration_band_summary.csv", index=False)

corr_cols = DEFENSES + ATTACHMENT + SELF_RELATIONAL + DERIVED + OUTCOMES
df[corr_cols].corr().to_csv(OUT / "python_psychodynamic_correlations.csv")

models = {
    "character_integration": ols(df, "character_integration", DEFENSES + ATTACHMENT + ["reflective_functioning"]),
    "self_relational_capacity": ols(df, "self_relational_capacity", ["defensive_maturity", "attachment_insecurity", "reflective_functioning"]),
    "symptom_distress": ols(df, "symptom_distress", ["hidden_structure_risk", "character_integration", "self_relational_capacity"]),
    "note": "Synthetic demonstration only; not clinical assessment, diagnosis, treatment planning, or individual interpretation.",
}
(OUT / "python_psychodynamic_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_psychodynamic_personality.csv", index=False)
print(f"Wrote outputs to {OUT}")
