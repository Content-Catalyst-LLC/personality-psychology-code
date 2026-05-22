#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_narrative_identity.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

THEMES = [
    "redemption",
    "contamination",
    "coherence",
    "agency",
    "communion",
    "meaning_making",
    "narrative_flexibility",
    "defensive_rigidity",
]
OUTCOMES = ["self_continuity", "well_being"]
DERIVED = [
    "narrative_growth_orientation",
    "narrative_burden",
    "narrative_integration",
    "redemptive_agency_balance",
]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "narrative_context", *THEMES, *OUTCOMES, *DERIVED}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["redemption_level"] = np.where(df["redemption"] > df["redemption"].median(), "higher_redemption", "lower_redemption")
df["contamination_level"] = np.where(df["contamination"] > df["contamination"].median(), "higher_contamination", "lower_contamination")
df["coherence_level"] = np.where(df["coherence"] > df["coherence"].median(), "higher_coherence", "lower_coherence")
df["narrative_profile"] = df["redemption_level"] + "_" + df["contamination_level"] + "_" + df["coherence_level"]

df["high_coherence_high_defensiveness"] = (
    (df["coherence"] > df["coherence"].median())
    & (df["defensive_rigidity"] > df["defensive_rigidity"].median())
)
df["high_contamination_low_continuity"] = (
    (df["contamination"] > df["contamination"].median())
    & (df["self_continuity"] < df["self_continuity"].median())
)

context_summary = (
    df.groupby("narrative_context")
    .agg(
        n=("person_id", "count"),
        redemption_mean=("redemption", "mean"),
        contamination_mean=("contamination", "mean"),
        coherence_mean=("coherence", "mean"),
        agency_mean=("agency", "mean"),
        communion_mean=("communion", "mean"),
        meaning_making_mean=("meaning_making", "mean"),
        narrative_flexibility_mean=("narrative_flexibility", "mean"),
        defensive_rigidity_mean=("defensive_rigidity", "mean"),
        self_continuity_mean=("self_continuity", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

profile_summary = (
    df.groupby("narrative_profile")
    .agg(
        n=("person_id", "count"),
        redemption_mean=("redemption", "mean"),
        contamination_mean=("contamination", "mean"),
        coherence_mean=("coherence", "mean"),
        agency_mean=("agency", "mean"),
        meaning_making_mean=("meaning_making", "mean"),
        self_continuity_mean=("self_continuity", "mean"),
        well_being_mean=("well_being", "mean"),
    )
    .reset_index()
)

pattern_summary = pd.DataFrame(
    {
        "pattern": ["high_coherence_high_defensiveness", "high_contamination_low_continuity"],
        "n": [int(df["high_coherence_high_defensiveness"].sum()), int(df["high_contamination_low_continuity"].sum())],
        "proportion": [float(df["high_coherence_high_defensiveness"].mean()), float(df["high_contamination_low_continuity"].mean())],
    }
)

corr_cols = THEMES + DERIVED + OUTCOMES
models = {
    "well_being": ols(df, "well_being", ["redemption", "contamination", "coherence", "agency", "communion", "meaning_making", "narrative_flexibility"]),
    "self_continuity": ols(df, "self_continuity", ["coherence", "redemption", "contamination", "meaning_making", "narrative_flexibility", "defensive_rigidity"]),
    "narrative_integration": ols(df, "narrative_integration", ["agency", "communion", "narrative_growth_orientation", "narrative_burden"]),
    "note": "Synthetic demonstration only; not clinical assessment, identity evaluation, personality testing, legal evaluation, workplace screening, or individual prediction.",
}

context_summary.to_csv(OUT / "python_narrative_context_summary.csv", index=False)
profile_summary.to_csv(OUT / "python_narrative_profile_summary.csv", index=False)
pattern_summary.to_csv(OUT / "python_narrative_pattern_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_narrative_identity_correlations.csv")
(OUT / "python_narrative_identity_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_narrative_identity.csv", index=False)
print(f"Wrote outputs to {OUT}")
