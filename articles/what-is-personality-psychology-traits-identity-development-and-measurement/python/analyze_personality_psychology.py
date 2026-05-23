#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PERSONALITY_DATA = ROOT / "data" / "synthetic_personality_items.csv"
STATE_DATA = ROOT / "data" / "synthetic_person_situation_observations.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

ITEMS = [f"item{i}" for i in range(1, 61)]
TRAIT_ITEM_GROUPS = {
    "conscientiousness": ["c1", "c2", "c3", "c4", "c5", "c6"],
    "extraversion": ["e1", "e2", "e3", "e4", "e5", "e6"],
    "neuroticism": ["n1", "n2", "n3", "n4", "n5", "n6"],
}
TRAIT_SCORES = ["conscientiousness_score", "extraversion_score", "neuroticism_score"]
OUTCOMES = ["identity_coherence", "life_satisfaction", "social_functioning", "developmental_integration"]
INDICES = ["measurement_reliability_index", "identity_trait_alignment_index", "person_situation_sensitivity_index", "responsible_interpretation_index"]

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

def standardized_pca_variance(frame: pd.DataFrame, n_components: int = 10) -> tuple[pd.DataFrame, np.ndarray]:
    X = frame.to_numpy(float)
    X = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    cov = np.cov(X, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    ratios = eigvals / eigvals.sum()
    scores = X @ eigvecs[:, :n_components]
    summary = pd.DataFrame({
        "component": list(range(1, n_components + 1)),
        "explained_variance_ratio": ratios[:n_components],
        "cumulative_explained_variance": np.cumsum(ratios[:n_components]),
    })
    return summary, scores

df = pd.read_csv(PERSONALITY_DATA)
state_df = pd.read_csv(STATE_DATA)

required_personality = {"person_id", *ITEMS, *sum(TRAIT_ITEM_GROUPS.values(), []), *TRAIT_SCORES, *OUTCOMES, *INDICES}
required_state = {"person_id", "occasion", "situation_type", "behavior_score", "trait_score", "situation_strength", "trait_x_situation", "observed_regulation", "contextual_constraint"}
missing_personality = required_personality - set(df.columns)
missing_state = required_state - set(state_df.columns)
if missing_personality:
    raise ValueError(f"Personality dataset missing columns: {sorted(missing_personality)}")
if missing_state:
    raise ValueError(f"Person-situation dataset missing columns: {sorted(missing_state)}")

# Re-score traits from item groups.
for trait, cols in TRAIT_ITEM_GROUPS.items():
    df[f"{trait}_rescored"] = df[cols].mean(axis=1)

pca_summary, component_scores = standardized_pca_variance(df[ITEMS], n_components=10)
for i in range(component_scores.shape[1]):
    df[f"personality_component_{i+1}"] = component_scores[:, i]

reliability = pd.DataFrame([
    {"scale": trait, "n_items": len(cols), "cronbach_alpha": cronbach_alpha(df[cols])}
    for trait, cols in TRAIT_ITEM_GROUPS.items()
] + [
    {"scale": "full_personality_item_pool_item1_item60", "n_items": 60, "cronbach_alpha": cronbach_alpha(df[ITEMS])}
])

trait_summary = df[TRAIT_SCORES + OUTCOMES + INDICES].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
correlations = df[TRAIT_SCORES + OUTCOMES + INDICES].corr()

person_state_summary = (
    state_df.groupby("person_id")
    .agg(
        mean_behavior_score=("behavior_score", "mean"),
        sd_behavior_score=("behavior_score", "std"),
        mean_trait_score=("trait_score", "mean"),
        mean_situation_strength=("situation_strength", "mean"),
        mean_trait_x_situation=("trait_x_situation", "mean"),
        mean_observed_regulation=("observed_regulation", "mean"),
        mean_contextual_constraint=("contextual_constraint", "mean"),
        n_observations=("occasion", "count"),
    )
    .reset_index()
)

merged = df.merge(person_state_summary, on="person_id", how="left")

models = {
    "identity_coherence_from_traits": ols(df, "identity_coherence", TRAIT_SCORES),
    "life_satisfaction_from_traits": ols(df, "life_satisfaction", TRAIT_SCORES),
    "social_functioning_from_traits": ols(df, "social_functioning", TRAIT_SCORES),
    "developmental_integration_from_traits_and_identity": ols(df, "developmental_integration", TRAIT_SCORES + ["identity_coherence"]),
    "responsible_interpretation_from_measurement_indices": ols(df, "responsible_interpretation_index", ["measurement_reliability_index", "identity_trait_alignment_index", "person_situation_sensitivity_index"]),
    "person_situation_behavior_model": ols(state_df, "behavior_score", ["trait_score", "situation_strength", "trait_x_situation", "observed_regulation", "contextual_constraint"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, consulting support, organizational learning, coaching reflection, and methodological comparison; not a standalone assessment, diagnosis, placement, screening, moral-labeling, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

trait_summary.to_csv(OUT / "python_trait_outcome_summary.csv", index=False)
correlations.to_csv(OUT / "python_trait_outcome_correlations.csv")
pca_summary.to_csv(OUT / "python_pca_dimensionality_summary.csv", index=False)
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
person_state_summary.to_csv(OUT / "python_person_situation_summary.csv", index=False)
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
merged.to_csv(OUT / "python_personality_merged_summary.csv", index=False)
print(f"Wrote outputs to {OUT}")
