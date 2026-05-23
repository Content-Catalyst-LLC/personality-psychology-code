#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_temperament_personality_longitudinal.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TEMPERAMENT = ["inhibition_t1", "negative_affect_t1", "surgency_t1", "effortful_control_t1"]
ENVIRONMENT = ["parenting_support_t1", "family_stress_t1", "classroom_support_t2", "peer_support_t2", "institutional_stability_t2"]
OUTCOMES = ["conscientiousness_t2", "neuroticism_t2", "social_confidence_t2", "regulation_skill_t2"]
DERIVED = ["reactivity_regulation_balance", "environmental_support_index", "developmental_risk_index", "adaptive_pathway_score"]

REQUIRED = {"child_id", "developmental_context", *TEMPERAMENT, *ENVIRONMENT, *OUTCOMES, *DERIVED}

def ols(df: pd.DataFrame, y: str, xs: list[str]) -> dict:
    model_df = df[[y] + xs].dropna()
    X = np.column_stack([np.ones(len(model_df)), model_df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, model_df[y].to_numpy(float), rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((model_df[y].to_numpy(float) - pred) ** 2))
    ss_tot = float(np.sum((model_df[y].to_numpy(float) - model_df[y].mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot else float("nan")
    return {"coefficients": dict(zip(["intercept", *xs], map(float, beta))), "r_squared": r2, "n": int(len(model_df))}

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

context_summary = (
    df.groupby("developmental_context")
    .agg(
        n=("child_id", "count"),
        inhibition_mean=("inhibition_t1", "mean"),
        negative_affect_mean=("negative_affect_t1", "mean"),
        surgency_mean=("surgency_t1", "mean"),
        effortful_control_mean=("effortful_control_t1", "mean"),
        parenting_support_mean=("parenting_support_t1", "mean"),
        family_stress_mean=("family_stress_t1", "mean"),
        classroom_support_mean=("classroom_support_t2", "mean"),
        conscientiousness_mean=("conscientiousness_t2", "mean"),
        neuroticism_mean=("neuroticism_t2", "mean"),
        social_confidence_mean=("social_confidence_t2", "mean"),
        regulation_skill_mean=("regulation_skill_t2", "mean"),
        developmental_risk_mean=("developmental_risk_index", "mean"),
        adaptive_pathway_mean=("adaptive_pathway_score", "mean"),
    )
    .reset_index()
)

correlations = df[TEMPERAMENT + ENVIRONMENT + OUTCOMES + DERIVED].corr()

df["inhibition_x_parenting_support"] = df["inhibition_t1"] * df["parenting_support_t1"]
df["negative_affect_x_family_stress"] = df["negative_affect_t1"] * df["family_stress_t1"]
df["effortful_control_x_classroom_support"] = df["effortful_control_t1"] * df["classroom_support_t2"]

models = {
    "conscientiousness_from_effortful_control_and_support": ols(df, "conscientiousness_t2", ["effortful_control_t1", "parenting_support_t1", "family_stress_t1", "classroom_support_t2"]),
    "neuroticism_from_inhibition_negative_affect_and_stress": ols(df, "neuroticism_t2", ["inhibition_t1", "negative_affect_t1", "parenting_support_t1", "family_stress_t1"]),
    "social_confidence_from_inhibition_surgency_and_support": ols(df, "social_confidence_t2", ["inhibition_t1", "surgency_t1", "classroom_support_t2", "peer_support_t2", "family_stress_t1"]),
    "regulation_skill_from_effortful_control_and_environment": ols(df, "regulation_skill_t2", ["effortful_control_t1", "parenting_support_t1", "classroom_support_t2", "family_stress_t1", "institutional_stability_t2"]),
    "risk_amplified_by_family_stress": ols(df, "developmental_risk_index", ["negative_affect_t1", "family_stress_t1", "negative_affect_x_family_stress", "effortful_control_t1"]),
    "regulation_supported_by_classroom_context": ols(df, "regulation_skill_t2", ["effortful_control_t1", "classroom_support_t2", "effortful_control_x_classroom_support", "parenting_support_t1"]),
    "professional_use_boundary": "Suitable for education, research prototyping, developmental formulation, teacher/parent education, consulting support, and methodological demonstration; not a standalone assessment, diagnosis, placement, prediction, or decision system."
}

context_summary.to_csv(OUT / "python_context_summary.csv", index=False)
correlations.to_csv(OUT / "python_temperament_personality_correlations.csv")
pd.DataFrame([{"model": k, "r_squared": v["r_squared"], "n": v["n"]} for k, v in models.items() if isinstance(v, dict)]).to_csv(OUT / "python_model_fit_summary.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_temperament_personality_longitudinal.csv", index=False)
print(f"Wrote outputs to {OUT}")
