#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_personality_lifespan.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAITS = ["neuroticism", "extraversion", "conscientiousness", "openness", "agreeableness"]
PROCESSES = ["role_investment", "state_practice_frequency", "perceived_support"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "wave", "wave_numeric", "age", "life_stage", "cohort", "cultural_context", *TRAITS, *PROCESSES}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

wave_summary = (
    df.groupby(["wave", "wave_numeric"])
    .agg(
        n=("person_id", "count"),
        mean_neuroticism=("neuroticism", "mean"),
        mean_extraversion=("extraversion", "mean"),
        mean_conscientiousness=("conscientiousness", "mean"),
        mean_openness=("openness", "mean"),
        mean_agreeableness=("agreeableness", "mean"),
        mean_role_investment=("role_investment", "mean"),
        mean_state_practice=("state_practice_frequency", "mean"),
        mean_perceived_support=("perceived_support", "mean"),
    )
    .reset_index()
)

life_stage_summary = (
    df.groupby(["life_stage"])
    .agg(
        n=("person_id", "count"),
        age_mean=("age", "mean"),
        neuroticism_mean=("neuroticism", "mean"),
        extraversion_mean=("extraversion", "mean"),
        conscientiousness_mean=("conscientiousness", "mean"),
        openness_mean=("openness", "mean"),
        agreeableness_mean=("agreeableness", "mean"),
        role_investment_mean=("role_investment", "mean"),
        perceived_support_mean=("perceived_support", "mean"),
    )
    .reset_index()
)

cohort_culture_summary = (
    df.groupby(["cohort", "cultural_context"])
    .agg(
        n=("person_id", "count"),
        neuroticism_mean=("neuroticism", "mean"),
        extraversion_mean=("extraversion", "mean"),
        conscientiousness_mean=("conscientiousness", "mean"),
        openness_mean=("openness", "mean"),
        agreeableness_mean=("agreeableness", "mean"),
        role_investment_mean=("role_investment", "mean"),
        perceived_support_mean=("perceived_support", "mean"),
    )
    .reset_index()
)

change_rows = []
wide_rows = []
for person_id, group in df.groupby("person_id"):
    ordered = group.sort_values("wave_numeric")
    first = ordered.iloc[0]
    last = ordered.iloc[-1]
    row = {
        "person_id": person_id,
        "cohort": first["cohort"],
        "cultural_context": first["cultural_context"],
        "age_first": first["age"],
        "age_last": last["age"],
        "role_investment_mean": ordered["role_investment"].mean(),
        "state_practice_mean": ordered["state_practice_frequency"].mean(),
        "perceived_support_mean": ordered["perceived_support"].mean(),
    }
    wide = {"person_id": person_id, "cohort": first["cohort"], "cultural_context": first["cultural_context"]}
    for trait in TRAITS:
        row[f"{trait}_change"] = last[trait] - first[trait]
        wide[f"{trait}_first"] = first[trait]
        wide[f"{trait}_last"] = last[trait]
    change_rows.append(row)
    wide_rows.append(wide)

change_summary = pd.DataFrame(change_rows)
wide_traits = pd.DataFrame(wide_rows)

rank_order_stability = pd.DataFrame({
    "trait": TRAITS,
    "rank_order_stability_first_last": [
        wide_traits[f"{trait}_first"].corr(wide_traits[f"{trait}_last"]) for trait in TRAITS
    ],
    "mean_level_change_first_last": [
        wide_traits[f"{trait}_last"].mean() - wide_traits[f"{trait}_first"].mean() for trait in TRAITS
    ],
})

model_data = pd.get_dummies(df, columns=["cohort", "cultural_context"], drop_first=True)
predictors = ["age", "role_investment", "state_practice_frequency", "perceived_support"] + [
    col for col in model_data.columns if col.startswith("cohort_") or col.startswith("cultural_context_")
]
models = {trait: ols(model_data, trait, predictors) for trait in TRAITS}
models["note"] = "Synthetic demonstration only; not clinical assessment, personality testing, coaching guidance, workplace screening, educational placement, or individual prediction."

wave_summary.to_csv(OUT / "python_wave_summary.csv", index=False)
life_stage_summary.to_csv(OUT / "python_life_stage_summary.csv", index=False)
cohort_culture_summary.to_csv(OUT / "python_cohort_culture_summary.csv", index=False)
change_summary.to_csv(OUT / "python_individual_change_summary.csv", index=False)
rank_order_stability.to_csv(OUT / "python_rank_order_stability.csv", index=False)
(OUT / "python_personality_lifespan_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_personality_lifespan.csv", index=False)
print(f"Wrote outputs to {OUT}")
