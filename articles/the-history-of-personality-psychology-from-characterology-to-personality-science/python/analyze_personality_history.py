#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_personality_history_items.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

ITEMS = [f"item{i}" for i in range(1, 61)]
C_ITEMS = [f"c{i}" for i in range(1, 7)]
TRAITS = [
    "extraversion_score",
    "agreeableness_score",
    "conscientiousness_score",
    "neuroticism_score",
    "openness_score",
]
HISTORY = [
    "characterology_typology_index",
    "psychometric_structure_index",
    "person_situation_index",
    "narrative_identity_index",
    "measurement_invariance_caution_index",
    "historical_method_maturity_index",
]
LONGITUDINAL = ["conscientiousness_t1", "conscientiousness_t2"]
INTERACTION = ["behavior_score", "trait_score", "situation_strength", "person_situation_interaction"]
REQUIRED = {"participant_id", *ITEMS, *C_ITEMS, *TRAITS, *HISTORY, *LONGITUDINAL, *INTERACTION}

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

def standardized_pca_variance(frame: pd.DataFrame, n_components: int = 10) -> tuple[pd.DataFrame, np.ndarray, pd.DataFrame]:
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
    loadings = pd.DataFrame(
        eigvecs[:, :n_components],
        index=frame.columns,
        columns=[f"component_{i}" for i in range(1, n_components + 1)],
    )
    return summary, scores, loadings

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Dataset missing columns: {sorted(missing)}")

df["conscientiousness_rescored"] = df[C_ITEMS].mean(axis=1)
df["stability_change"] = df["conscientiousness_t2"] - df["conscientiousness_t1"]

pca_summary, component_scores, loadings = standardized_pca_variance(df[ITEMS], n_components=10)
for i in range(component_scores.shape[1]):
    df[f"component_{i+1}"] = component_scores[:, i]

trait_summary = df[TRAITS + LONGITUDINAL + INTERACTION].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
history_summary = df[HISTORY + ["stability_change"]].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
correlations = df[TRAITS + HISTORY + LONGITUDINAL + INTERACTION].corr()

reliability = pd.DataFrame([
    {"scale": "conscientiousness_c1_c6", "level": "short_trait_scale", "n_items": 6, "cronbach_alpha": cronbach_alpha(df[C_ITEMS])},
    {"scale": "full_personality_item_pool_item1_item60", "level": "broad_item_pool", "n_items": 60, "cronbach_alpha": cronbach_alpha(df[ITEMS])},
])

models = {
    "conscientiousness_stability_t2_from_t1": ols(df, "conscientiousness_t2", ["conscientiousness_t1"]),
    "behavior_from_trait_situation_interaction": ols(df, "behavior_score", ["trait_score", "situation_strength", "person_situation_interaction"]),
    "psychometric_structure_from_traits": ols(df, "psychometric_structure_index", TRAITS),
    "historical_method_maturity_from_components": ols(df, "historical_method_maturity_index", ["psychometric_structure_index", "person_situation_index", "narrative_identity_index", "measurement_invariance_caution_index"]),
    "typology_residual_from_low_method_maturity": ols(df, "characterology_typology_index", ["psychometric_structure_index", "historical_method_maturity_index"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, consulting support, organizational learning, coaching reflection, and methodological comparison; not a standalone assessment, diagnosis, placement, screening, moral-labeling, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

stability_correlation = float(df[["conscientiousness_t1", "conscientiousness_t2"]].corr().iloc[0, 1])
stability_summary = pd.DataFrame([
    {
        "measure": "conscientiousness_rank_order_stability",
        "correlation": stability_correlation,
        "mean_t1": df["conscientiousness_t1"].mean(),
        "mean_t2": df["conscientiousness_t2"].mean(),
        "mean_change": df["stability_change"].mean(),
        "sd_change": df["stability_change"].std(ddof=1),
    }
])

trait_summary.to_csv(OUT / "python_trait_summary.csv", index=False)
history_summary.to_csv(OUT / "python_history_index_summary.csv", index=False)
correlations.to_csv(OUT / "python_personality_history_correlations.csv")
pca_summary.to_csv(OUT / "python_pca_dimensionality_summary.csv", index=False)
loadings.to_csv(OUT / "python_pca_loadings.csv")
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
stability_summary.to_csv(OUT / "python_stability_summary.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_personality_history_items.csv", index=False)
print(f"Wrote outputs to {OUT}")
