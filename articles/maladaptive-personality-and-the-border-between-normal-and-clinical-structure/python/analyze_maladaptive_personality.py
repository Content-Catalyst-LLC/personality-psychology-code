#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_maladaptive_personality_structure.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAITS = ["negative_affectivity", "detachment", "antagonism", "disinhibition", "psychoticism", "anankastia"]
FUNCTIONING = ["identity_impairment", "self_direction_impairment", "empathy_impairment", "intimacy_impairment"]
BOUNDARY = ["rigidity", "pervasiveness", "contextual_stress", "perceived_support"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"participant_id", "clinical_context", *TRAITS, *FUNCTIONING, "clinical_severity", "clinical_liability", "threshold_zone_indicator", *BOUNDARY}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

df["dominant_trait_domain"] = df[TRAITS].idxmax(axis=1)
df["severity_band"] = np.select(
    [df["clinical_severity"] < 2.5, df["clinical_severity"].between(2.5, 4.5, inclusive="left"), df["clinical_severity"] >= 4.5],
    ["lower_severity", "moderate_severity", "higher_severity"],
    default="unclassified"
)
df["threshold_status"] = np.where(df["clinical_liability"] >= df["clinical_liability"].quantile(.75), "higher_clinical_liability", "lower_or_moderate_liability")

df.groupby("clinical_context").agg(
    n=("participant_id", "count"),
    functioning_impairment_mean=("functioning_impairment", "mean"),
    trait_burden_mean=("maladaptive_trait_burden", "mean"),
    rigidity_mean=("rigidity", "mean"),
    pervasiveness_mean=("pervasiveness", "mean"),
    clinical_severity_mean=("clinical_severity", "mean"),
    clinical_liability_mean=("clinical_liability", "mean"),
).reset_index().to_csv(OUT / "python_clinical_context_summary.csv", index=False)

df.groupby("severity_band").agg(
    n=("participant_id", "count"),
    trait_burden_mean=("maladaptive_trait_burden", "mean"),
    functioning_impairment_mean=("functioning_impairment", "mean"),
    rigidity_mean=("rigidity", "mean"),
    pervasiveness_mean=("pervasiveness", "mean"),
    threshold_zone_mean=("threshold_zone_indicator", "mean"),
).reset_index().to_csv(OUT / "python_severity_band_summary.csv", index=False)

df.groupby("dominant_trait_domain").agg(
    n=("participant_id", "count"),
    clinical_severity_mean=("clinical_severity", "mean"),
    functioning_impairment_mean=("functioning_impairment", "mean"),
    clinical_liability_mean=("clinical_liability", "mean"),
).reset_index().to_csv(OUT / "python_dominant_trait_domain_summary.csv", index=False)

corr_cols = TRAITS + FUNCTIONING + ["functioning_impairment", "maladaptive_trait_burden", "severity_trait_interaction", "clinical_severity", "clinical_liability", "threshold_zone_indicator"] + BOUNDARY
df[corr_cols].corr().to_csv(OUT / "python_maladaptive_personality_correlations.csv")

models = {
    "clinical_severity": ols(df, "clinical_severity", TRAITS + ["functioning_impairment"]),
    "clinical_liability": ols(df, "clinical_liability", ["maladaptive_trait_burden", "functioning_impairment", "rigidity", "pervasiveness", "contextual_stress", "perceived_support"]),
    "threshold_zone_indicator": ols(df, "threshold_zone_indicator", ["maladaptive_trait_burden", "functioning_impairment", "rigidity", "pervasiveness", "contextual_stress", "perceived_support"]),
    "note": "Synthetic demonstration only; not diagnosis, screening, clinical decision support, or risk scoring."
}
(OUT / "python_maladaptive_personality_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_maladaptive_personality.csv", index=False)
print(f"Wrote outputs to {OUT}")
