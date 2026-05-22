#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_personality_dynamics_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAITS = ["trait_extraversion", "trait_conscientiousness", "trait_neuroticism"]
STATES = ["state_extraversion", "state_conscientiousness", "state_neuroticism"]
SITUATIONS = ["situation_valence", "situation_sociality", "situation_demand", "situation_evaluation"]
PROCESSES = ["positive_affect", "negative_affect", "goal_pressure", "autonomy_support"]

REQUIRED = {
    "person_id",
    "assessment_context",
    "occasion",
    *TRAITS,
    *STATES,
    *SITUATIONS,
    *PROCESSES,
    "state_inertia_marker",
    "dynamic_signature_score",
}

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

for variable in SITUATIONS:
    person_mean = f"{variable}_person_mean"
    within = f"{variable}_within"
    df[person_mean] = df.groupby("person_id")[variable].transform("mean")
    df[within] = df[variable] - df[person_mean]

for state in STATES:
    df[f"lag_{state}"] = df.groupby("person_id")[state].shift(1)
    df[f"{state}_within_deviation"] = df[state] - df.groupby("person_id")[state].transform("mean")

person_summary = (
    df.groupby(["person_id", "assessment_context"])
    .agg(
        n_obs=("occasion", "count"),
        trait_extraversion=("trait_extraversion", "mean"),
        trait_conscientiousness=("trait_conscientiousness", "mean"),
        trait_neuroticism=("trait_neuroticism", "mean"),
        mean_state_extraversion=("state_extraversion", "mean"),
        sd_state_extraversion=("state_extraversion", "std"),
        mean_state_conscientiousness=("state_conscientiousness", "mean"),
        sd_state_conscientiousness=("state_conscientiousness", "std"),
        mean_state_neuroticism=("state_neuroticism", "mean"),
        sd_state_neuroticism=("state_neuroticism", "std"),
        mean_positive_affect=("positive_affect", "mean"),
        sd_positive_affect=("positive_affect", "std"),
        mean_negative_affect=("negative_affect", "mean"),
        sd_negative_affect=("negative_affect", "std"),
        mean_dynamic_signature=("dynamic_signature_score", "mean"),
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
        state_extraversion_sd=("state_extraversion", "std"),
        state_conscientiousness_mean=("state_conscientiousness", "mean"),
        state_neuroticism_mean=("state_neuroticism", "mean"),
        situation_sociality_mean=("situation_sociality", "mean"),
        situation_demand_mean=("situation_demand", "mean"),
        situation_evaluation_mean=("situation_evaluation", "mean"),
        dynamic_signature_mean=("dynamic_signature_score", "mean"),
    )
    .reset_index()
)

# Approximate intraclass-correlation style summaries.
icc_rows = []
for state in STATES:
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

# Person-level situation sensitivity approximations via simple within-person slopes.
sensitivity_rows = []
for person_id, sub in df.groupby("person_id"):
    row = {"person_id": person_id}
    for situation, state in [
        ("situation_sociality_within", "state_extraversion"),
        ("situation_demand_within", "state_conscientiousness"),
        ("situation_evaluation_within", "state_neuroticism"),
    ]:
        if sub[situation].std(ddof=1) > 0:
            row[f"{state}_slope_for_{situation}"] = float(np.cov(sub[situation], sub[state], ddof=1)[0, 1] / sub[situation].var(ddof=1))
        else:
            row[f"{state}_slope_for_{situation}"] = float("nan")
    sensitivity_rows.append(row)
situation_sensitivity = pd.DataFrame(sensitivity_rows)

lag_df = df.dropna(subset=["lag_state_extraversion", "lag_state_conscientiousness", "lag_state_neuroticism"]).copy()

models = {
    "state_extraversion_situational": ols(
        df,
        "state_extraversion",
        ["trait_extraversion", "situation_sociality_within", "situation_valence_within", "autonomy_support"],
    ),
    "state_conscientiousness_situational": ols(
        df,
        "state_conscientiousness",
        ["trait_conscientiousness", "situation_demand_within", "goal_pressure", "autonomy_support"],
    ),
    "state_neuroticism_situational": ols(
        df,
        "state_neuroticism",
        ["trait_neuroticism", "situation_evaluation_within", "situation_valence_within", "negative_affect"],
    ),
    "state_extraversion_inertia": ols(
        lag_df,
        "state_extraversion",
        ["lag_state_extraversion", "situation_sociality_within", "positive_affect"],
    ),
    "professional_use_boundary": "Suitable for education, research prototyping, consulting support, organizational learning, and methodological demonstration; not a standalone assessment or decision system for consequential individual decisions.",
}

person_summary.to_csv(OUT / "python_person_summary.csv", index=False)
context_summary.to_csv(OUT / "python_context_summary.csv", index=False)
icc_summary.to_csv(OUT / "python_icc_like_summary.csv", index=False)
situation_sensitivity.to_csv(OUT / "python_situation_sensitivity.csv", index=False)
df.to_csv(OUT / "python_scored_personality_dynamics_data.csv", index=False)
df[TRAITS + STATES + SITUATIONS + PROCESSES + ["state_inertia_marker", "dynamic_signature_score"]].corr().to_csv(OUT / "python_dynamic_correlations.csv")
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
print(f"Wrote outputs to {OUT}")
