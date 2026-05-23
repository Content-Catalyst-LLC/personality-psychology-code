#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRAIT_DATA = ROOT / "data" / "synthetic_trait_items.csv"
STATE_DATA = ROOT / "data" / "synthetic_state_observations.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TRAIT_ITEM_GROUPS = {
    "conscientiousness": ["c1", "c2", "c3", "c4", "c5", "c6"],
    "extraversion": ["e1", "e2", "e3", "e4", "e5", "e6"],
    "neuroticism": ["n1", "n2", "n3", "n4", "n5", "n6"],
}
TRAIT_SCORES = ["conscientiousness_score", "extraversion_score", "neuroticism_score"]
STATE_SCORES = ["state_conscientiousness", "state_extraversion", "state_neuroticism"]

def cronbach_alpha(frame: pd.DataFrame) -> float:
    clean = frame.dropna()
    n_items = clean.shape[1]
    if n_items <= 1:
        return float("nan")
    item_variances = clean.var(axis=0, ddof=1)
    total_score = clean.sum(axis=1)
    total_var = total_score.var(ddof=1)
    return float((n_items / (n_items - 1)) * (1 - item_variances.sum() / total_var)) if total_var else float("nan")

def ols(df: pd.DataFrame, y: str, xs: list[str]) -> dict:
    model_df = df[[y] + xs].dropna()
    X = np.column_stack([np.ones(len(model_df)), model_df[xs].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, model_df[y].to_numpy(float), rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((model_df[y].to_numpy(float) - pred) ** 2))
    ss_tot = float(np.sum((model_df[y].to_numpy(float) - model_df[y].mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot else float("nan")
    return {"coefficients": dict(zip(["intercept", *xs], map(float, beta))), "r_squared": r2, "n": int(len(model_df))}

trait_df = pd.read_csv(TRAIT_DATA)
state_df = pd.read_csv(STATE_DATA)

required_trait = {"person_id", *sum(TRAIT_ITEM_GROUPS.values(), []), *TRAIT_SCORES}
required_state = {"person_id", "occasion", "situation_type", *STATE_SCORES, "situational_activation", "situational_constraint"}
missing_trait = required_trait - set(trait_df.columns)
missing_state = required_state - set(state_df.columns)
if missing_trait:
    raise ValueError(f"Trait dataset missing columns: {sorted(missing_trait)}")
if missing_state:
    raise ValueError(f"State dataset missing columns: {sorted(missing_state)}")

# Re-score traits from item groups.
for trait, cols in TRAIT_ITEM_GROUPS.items():
    trait_df[f"{trait}_rescored"] = trait_df[cols].mean(axis=1)

reliability = pd.DataFrame([
    {
        "scale": trait,
        "n_items": len(cols),
        "cronbach_alpha": cronbach_alpha(trait_df[cols]),
    }
    for trait, cols in TRAIT_ITEM_GROUPS.items()
])

person_summary = (
    state_df.groupby("person_id")
    .agg(
        mean_state_conscientiousness=("state_conscientiousness", "mean"),
        sd_state_conscientiousness=("state_conscientiousness", "std"),
        mean_state_extraversion=("state_extraversion", "mean"),
        sd_state_extraversion=("state_extraversion", "std"),
        mean_state_neuroticism=("state_neuroticism", "mean"),
        sd_state_neuroticism=("state_neuroticism", "std"),
        mean_situational_activation=("situational_activation", "mean"),
        mean_situational_constraint=("situational_constraint", "mean"),
        n_observations=("occasion", "count"),
    )
    .reset_index()
)

merged = trait_df.merge(person_summary, on="person_id", how="inner")
merged["trait_state_alignment_index"] = (
    10
    - (
        (merged["conscientiousness_score"] - merged["mean_state_conscientiousness"]).abs()
        + (merged["extraversion_score"] - merged["mean_state_extraversion"]).abs()
        + (merged["neuroticism_score"] - merged["mean_state_neuroticism"]).abs()
    )
).clip(lower=0, upper=10)
merged["state_variability_index"] = (
    merged["sd_state_conscientiousness"]
    + merged["sd_state_extraversion"]
    + merged["sd_state_neuroticism"]
).clip(lower=0, upper=10)
merged["person_situation_sensitivity_index"] = (
    merged["mean_situational_activation"] * 0.45
    + merged["mean_situational_constraint"] * 0.35
    + merged["state_variability_index"] * 0.20
).clip(lower=0, upper=10)
merged["aggregation_reliability_index"] = (
    np.sqrt(merged["n_observations"]) * 1.15
    + merged["trait_state_alignment_index"] * 0.35
    - merged["state_variability_index"] * 0.18
).clip(lower=0, upper=10)

trait_summary = trait_df[TRAIT_SCORES + ["self_report_consistency_index", "trait_observation_alignment"]].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
state_summary = state_df[STATE_SCORES + ["situational_activation", "situational_constraint"]].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
person_summary_table = merged[
    TRAIT_SCORES
    + [
        "mean_state_conscientiousness",
        "sd_state_conscientiousness",
        "mean_state_extraversion",
        "sd_state_extraversion",
        "mean_state_neuroticism",
        "sd_state_neuroticism",
        "trait_state_alignment_index",
        "state_variability_index",
        "person_situation_sensitivity_index",
        "aggregation_reliability_index",
    ]
].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})

trait_state_correlations = merged[
    [
        "conscientiousness_score",
        "mean_state_conscientiousness",
        "extraversion_score",
        "mean_state_extraversion",
        "neuroticism_score",
        "mean_state_neuroticism",
        "trait_state_alignment_index",
        "state_variability_index",
    ]
].corr()

# Variance decomposition approximation.
variance_components = []
for state_col in STATE_SCORES:
    person_means = state_df.groupby("person_id")[state_col].mean()
    between = float(person_means.var(ddof=1))
    within = float(state_df.groupby("person_id")[state_col].var(ddof=1).mean())
    total = between + within
    variance_components.append({
        "state_variable": state_col,
        "between_person_variance": between,
        "within_person_variance": within,
        "between_person_share": between / total if total else np.nan,
        "within_person_share": within / total if total else np.nan,
    })
variance_components = pd.DataFrame(variance_components)

models = {
    "mean_state_conscientiousness_from_trait": ols(merged, "mean_state_conscientiousness", ["conscientiousness_score"]),
    "mean_state_extraversion_from_trait": ols(merged, "mean_state_extraversion", ["extraversion_score"]),
    "mean_state_neuroticism_from_trait": ols(merged, "mean_state_neuroticism", ["neuroticism_score"]),
    "trait_state_alignment_from_variability": ols(merged, "trait_state_alignment_index", ["state_variability_index", "person_situation_sensitivity_index", "aggregation_reliability_index"]),
    "state_variability_from_situation": ols(merged, "state_variability_index", ["mean_situational_activation", "mean_situational_constraint"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, consulting support, organizational learning, coaching reflection, and methodological comparison; not a standalone assessment, diagnosis, placement, screening, moral-labeling, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

trait_summary.to_csv(OUT / "python_trait_summary.csv", index=False)
state_summary.to_csv(OUT / "python_state_summary.csv", index=False)
person_summary_table.to_csv(OUT / "python_person_level_summary.csv", index=False)
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
trait_state_correlations.to_csv(OUT / "python_trait_state_correlations.csv")
variance_components.to_csv(OUT / "python_variance_components.csv", index=False)
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
merged.to_csv(OUT / "python_trait_state_merged.csv", index=False)
print(f"Wrote outputs to {OUT}")
