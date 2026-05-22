#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_person_situation_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

PERSON_COLS = ["trait_score", "trait_extraversion", "trait_conscientiousness", "trait_neuroticism"]
STATE_COLS = ["state_extraversion", "state_conscientiousness", "state_assertiveness", "state_withdrawal"]
SITUATION_COLS = [
    "situation_demand",
    "situation_sociality",
    "situation_evaluation",
    "situation_trust",
    "situation_autonomy",
    "situation_threat",
]
DERIVED = ["behavioral_consistency_marker", "conditional_signature_score", "state_inertia_marker"]

REQUIRED = {"person_id", "assessment_context", "occasion", *PERSON_COLS, *STATE_COLS, *SITUATION_COLS, *DERIVED}

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

df = df.sort_values(["person_id", "occasion"]).copy()

# Within-person centering for situational predictors.
for variable in SITUATION_COLS:
    person_mean = f"{variable}_person_mean"
    within = f"{variable}_within"
    df[person_mean] = df.groupby("person_id")[variable].transform("mean")
    df[within] = df[variable] - df[person_mean]

# Lagged state variables for inertia.
for state in STATE_COLS:
    df[f"lag_{state}"] = df.groupby("person_id")[state].shift(1)
    df[f"{state}_within_deviation"] = df[state] - df.groupby("person_id")[state].transform("mean")

person_summary = (
    df.groupby(["person_id", "assessment_context"])
    .agg(
        n_obs=("occasion", "count"),
        trait_score=("trait_score", "mean"),
        trait_extraversion=("trait_extraversion", "mean"),
        trait_conscientiousness=("trait_conscientiousness", "mean"),
        trait_neuroticism=("trait_neuroticism", "mean"),
        mean_state_extraversion=("state_extraversion", "mean"),
        sd_state_extraversion=("state_extraversion", "std"),
        mean_state_conscientiousness=("state_conscientiousness", "mean"),
        sd_state_conscientiousness=("state_conscientiousness", "std"),
        mean_state_assertiveness=("state_assertiveness", "mean"),
        sd_state_assertiveness=("state_assertiveness", "std"),
        mean_state_withdrawal=("state_withdrawal", "mean"),
        sd_state_withdrawal=("state_withdrawal", "std"),
        mean_behavioral_consistency_marker=("behavioral_consistency_marker", "mean"),
        mean_conditional_signature_score=("conditional_signature_score", "mean"),
        mean_state_inertia_marker=("state_inertia_marker", "mean"),
    )
    .reset_index()
)

context_summary = (
    df.groupby("assessment_context")
    .agg(
        n_persons=("person_id", "nunique"),
        n_observations=("occasion", "count"),
        state_extraversion_mean=("state_extraversion", "mean"),
        state_conscientiousness_mean=("state_conscientiousness", "mean"),
        state_assertiveness_mean=("state_assertiveness", "mean"),
        state_withdrawal_mean=("state_withdrawal", "mean"),
        situation_demand_mean=("situation_demand", "mean"),
        situation_sociality_mean=("situation_sociality", "mean"),
        situation_evaluation_mean=("situation_evaluation", "mean"),
        conditional_signature_mean=("conditional_signature_score", "mean"),
        behavioral_consistency_mean=("behavioral_consistency_marker", "mean"),
    )
    .reset_index()
)

# Approximate ICC-style summaries.
icc_rows = []
for state in STATE_COLS:
    person_means = df.groupby("person_id")[state].mean()
    merged = df.merge(person_means.rename(f"{state}_person_mean"), left_on="person_id", right_index=True)
    between = float(person_means.var(ddof=1))
    within = float((merged[state] - merged[f"{state}_person_mean"]).var(ddof=1))
    icc = between / (between + within) if (between + within) else float("nan")
    icc_rows.append({
        "state": state,
        "between_person_variance": between,
        "within_person_variance": within,
        "icc_like_ratio": icc,
    })
icc_summary = pd.DataFrame(icc_rows)

# Person-level sensitivity approximations.
sensitivity_rows = []
for person_id, sub in df.groupby("person_id"):
    row = {"person_id": person_id}
    pairs = [
        ("situation_sociality_within", "state_extraversion"),
        ("situation_demand_within", "state_conscientiousness"),
        ("situation_evaluation_within", "state_assertiveness"),
        ("situation_threat_within", "state_withdrawal"),
    ]
    for situation, state in pairs:
        if sub[situation].std(ddof=1) > 0:
            row[f"{state}_slope_for_{situation}"] = float(np.cov(sub[situation], sub[state], ddof=1)[0, 1] / sub[situation].var(ddof=1))
        else:
            row[f"{state}_slope_for_{situation}"] = float("nan")
    sensitivity_rows.append(row)
situation_sensitivity = pd.DataFrame(sensitivity_rows)

lag_df = df.dropna(subset=["lag_state_extraversion", "lag_state_conscientiousness", "lag_state_assertiveness", "lag_state_withdrawal"]).copy()

models = {
    "state_extraversion_person_situation": ols(
        df,
        "state_extraversion",
        ["trait_extraversion", "situation_sociality_within", "situation_trust_within", "situation_autonomy_within"],
    ),
    "state_conscientiousness_demand": ols(
        df,
        "state_conscientiousness",
        ["trait_conscientiousness", "situation_demand_within", "situation_evaluation_within", "situation_autonomy_within"],
    ),
    "assertiveness_evaluation_trust": ols(
        df,
        "state_assertiveness",
        ["trait_score", "situation_evaluation_within", "situation_trust_within", "situation_threat_within"],
    ),
    "withdrawal_threat": ols(
        df,
        "state_withdrawal",
        ["trait_neuroticism", "situation_threat_within", "situation_evaluation_within", "situation_trust_within"],
    ),
    "state_extraversion_inertia": ols(
        lag_df,
        "state_extraversion",
        ["lag_state_extraversion", "situation_sociality_within", "situation_trust_within"],
    ),
    "professional_use_boundary": "Suitable for education, research prototyping, consulting support, organizational learning, and methodological demonstration; not a standalone assessment or decision system for consequential individual decisions.",
}

person_summary.to_csv(OUT / "python_person_summary.csv", index=False)
context_summary.to_csv(OUT / "python_context_summary.csv", index=False)
icc_summary.to_csv(OUT / "python_icc_like_summary.csv", index=False)
situation_sensitivity.to_csv(OUT / "python_situation_sensitivity.csv", index=False)
df.to_csv(OUT / "python_scored_person_situation_data.csv", index=False)
df[PERSON_COLS + STATE_COLS + SITUATION_COLS + DERIVED].corr().to_csv(OUT / "python_person_situation_correlations.csv")
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
print(f"Wrote outputs to {OUT}")
