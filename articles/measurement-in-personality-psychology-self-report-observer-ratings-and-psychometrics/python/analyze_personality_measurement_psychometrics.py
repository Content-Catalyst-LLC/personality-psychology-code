#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_personality_measurement_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

SELF_ITEMS = ["s1", "s2", "s3", "s4", "s5"]
OBSERVER_ITEMS = ["o1", "o2", "o3", "o4", "o5"]
REQUIRED = {
    "person_id",
    "assessment_context",
    *SELF_ITEMS,
    *OBSERVER_ITEMS,
    "attention_check",
    "careless_response_risk",
    "social_desirability_pressure",
    "self_missing_count",
    "observer_missing_count",
    "self_conscientiousness",
    "observer_conscientiousness",
    "self_other_discrepancy",
    "absolute_self_other_discrepancy",
    "method_effect_index",
    "reliability_context_score",
    "professional_reflection_score",
}

def cronbach_alpha(frame: pd.DataFrame) -> float:
    clean = frame.dropna()
    k = clean.shape[1]
    if len(clean) < 3 or k < 2:
        return float("nan")
    item_variances = clean.var(axis=0, ddof=1).sum()
    total_variance = clean.sum(axis=1).var(ddof=1)
    if total_variance == 0:
        return float("nan")
    return float((k / (k - 1)) * (1 - item_variances / total_variance))

def ols(df: pd.DataFrame, y: str, xs: list[str]) -> dict:
    model_df = df[[y] + xs].dropna()
    X = np.column_stack([np.ones(len(model_df)), model_df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, model_df[y].to_numpy(float), rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((model_df[y].to_numpy(float) - pred) ** 2))
    ss_tot = float(np.sum((model_df[y].to_numpy(float) - model_df[y].mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot else float("nan")
    return {
        "coefficients": dict(zip(["intercept", *xs], map(float, beta))),
        "r_squared": r2,
        "n": int(len(model_df)),
    }

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

self_alpha = cronbach_alpha(df[SELF_ITEMS])
observer_alpha = cronbach_alpha(df[OBSERVER_ITEMS])
self_other_agreement = float(df[["self_conscientiousness", "observer_conscientiousness"]].corr().iloc[0, 1])

filtered = df[
    (df["attention_check"] == 1)
    & (df["self_missing_count"] <= 2)
    & (df["observer_missing_count"] <= 2)
].copy()

filtered_agreement = float(filtered[["self_conscientiousness", "observer_conscientiousness"]].corr().iloc[0, 1])

context_summary = (
    df.groupby("assessment_context")
    .agg(
        n=("person_id", "count"),
        attention_pass_rate=("attention_check", "mean"),
        careless_response_risk_mean=("careless_response_risk", "mean"),
        social_desirability_pressure_mean=("social_desirability_pressure", "mean"),
        self_conscientiousness_mean=("self_conscientiousness", "mean"),
        observer_conscientiousness_mean=("observer_conscientiousness", "mean"),
        absolute_discrepancy_mean=("absolute_self_other_discrepancy", "mean"),
        method_effect_mean=("method_effect_index", "mean"),
        reliability_context_mean=("reliability_context_score", "mean"),
        professional_reflection_mean=("professional_reflection_score", "mean"),
    )
    .reset_index()
)

item_summary = []
for item in SELF_ITEMS + OBSERVER_ITEMS:
    item_summary.append({
        "item": item,
        "mean": float(df[item].mean(skipna=True)),
        "std": float(df[item].std(skipna=True)),
        "missing_rate": float(df[item].isna().mean()),
        "source": "self_report" if item.startswith("s") else "observer_report",
    })
item_summary = pd.DataFrame(item_summary)

discrepancy_summary = pd.DataFrame({
    "metric": [
        "n",
        "self_report_alpha",
        "observer_report_alpha",
        "self_other_agreement",
        "filtered_self_other_agreement",
        "mean_absolute_self_other_discrepancy",
        "attention_pass_rate",
        "mean_method_effect_index",
    ],
    "value": [
        len(df),
        self_alpha,
        observer_alpha,
        self_other_agreement,
        filtered_agreement,
        float(df["absolute_self_other_discrepancy"].mean()),
        float(df["attention_check"].mean()),
        float(df["method_effect_index"].mean()),
    ],
})

models = {
    "observer_from_self": ols(df, "observer_conscientiousness", ["self_conscientiousness"]),
    "absolute_discrepancy_from_method_context": ols(
        df,
        "absolute_self_other_discrepancy",
        ["careless_response_risk", "social_desirability_pressure", "method_effect_index"],
    ),
    "professional_reflection": ols(
        df,
        "professional_reflection_score",
        ["reliability_context_score", "method_effect_index", "absolute_self_other_discrepancy"],
    ),
    "professional_use_boundary": "Suitable for education, research prototyping, consulting support, organizational learning, and methodological demonstration; not a standalone assessment or decision system for consequential individual decisions.",
}

corr_cols = SELF_ITEMS + OBSERVER_ITEMS + [
    "self_conscientiousness",
    "observer_conscientiousness",
    "self_other_discrepancy",
    "absolute_self_other_discrepancy",
    "careless_response_risk",
    "social_desirability_pressure",
    "method_effect_index",
    "reliability_context_score",
    "professional_reflection_score",
]

context_summary.to_csv(OUT / "python_context_summary.csv", index=False)
item_summary.to_csv(OUT / "python_item_summary.csv", index=False)
discrepancy_summary.to_csv(OUT / "python_reliability_agreement_summary.csv", index=False)
df[corr_cols].corr().to_csv(OUT / "python_measurement_correlations.csv")
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_personality_measurement_data.csv", index=False)
print(f"Wrote outputs to {OUT}")
