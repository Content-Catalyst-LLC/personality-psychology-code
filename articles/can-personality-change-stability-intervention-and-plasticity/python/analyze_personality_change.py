#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_personality_change_intervention.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAITS = ["neuroticism", "extraversion", "conscientiousness", "openness", "agreeableness"]
PROCESSES = ["role_investment", "state_practice_frequency", "perceived_support"]

def ols(df, y, xs):
    X = np.column_stack([np.ones(len(df)), df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, df[y].to_numpy(float), rcond=None)
    return dict(zip(["intercept", *xs], map(float, beta)))

df = pd.read_csv(DATA)
required = {"person_id", "wave", "wave_numeric", "intervention_group", "age", *TRAITS, *PROCESSES}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

wave_summary = (
    df.groupby(["wave", "wave_numeric", "intervention_group"])
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

change_rows = []
wide_rows = []
for person_id, group in df.groupby("person_id"):
    ordered = group.sort_values("wave_numeric")
    first = ordered.iloc[0]
    last = ordered.iloc[-1]
    row = {
        "person_id": person_id,
        "intervention_group": first["intervention_group"],
        "age_first": first["age"],
        "age_last": last["age"],
        "role_investment_mean": ordered["role_investment"].mean(),
        "state_practice_mean": ordered["state_practice_frequency"].mean(),
        "perceived_support_mean": ordered["perceived_support"].mean(),
    }
    wide = {"person_id": person_id, "intervention_group": first["intervention_group"]}
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

model_data = df.copy()
model_data["intervention_binary"] = (model_data["intervention_group"] == "intervention").astype(int)
model_data["wave_x_intervention"] = model_data["wave_numeric"] * model_data["intervention_binary"]

predictors = ["wave_numeric", "intervention_binary", "wave_x_intervention", "age", "role_investment", "state_practice_frequency", "perceived_support"]
models = {trait: ols(model_data, trait, predictors) for trait in TRAITS}
models["note"] = "Synthetic demonstration only; not clinical assessment, personality testing, coaching guidance, workplace screening, educational placement, or individual prediction."

wave_summary.to_csv(OUT / "python_wave_summary.csv", index=False)
change_summary.to_csv(OUT / "python_individual_change_summary.csv", index=False)
rank_order_stability.to_csv(OUT / "python_rank_order_stability.csv", index=False)
(OUT / "python_personality_change_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_personality_change.csv", index=False)
print(f"Wrote outputs to {OUT}")
