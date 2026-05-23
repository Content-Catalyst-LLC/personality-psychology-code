#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_lexical_descriptors.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

DESCRIPTORS = [f"adj{i}" for i in range(1, 101)]
CLUSTERS = [
    "sociable_cluster_score",
    "reliable_cluster_score",
    "compassionate_cluster_score",
    "anxious_cluster_score",
    "imaginative_cluster_score",
]
CRITERIA = [
    "social_reliability_outcome",
    "interpersonal_trust_outcome",
    "expressive_engagement_outcome",
    "lexical_visibility_index",
]
DERIVED = [
    "lexical_abundance_index",
    "structural_centrality_index",
    "descriptor_redundancy_index",
    "cross_language_caution_index",
]
REQUIRED = {"respondent_id", *DESCRIPTORS, *CLUSTERS, *CRITERIA, *DERIVED}

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

def standardized_pca_variance(frame: pd.DataFrame, n_components: int = 12) -> tuple[pd.DataFrame, np.ndarray]:
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

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

# Re-score visible lexical clusters from descriptor blocks.
cluster_map = {
    "sociable_rescored": [f"adj{i}" for i in range(1, 21)],
    "reliable_rescored": [f"adj{i}" for i in range(21, 41)],
    "compassionate_rescored": [f"adj{i}" for i in range(41, 61)],
    "anxious_rescored": [f"adj{i}" for i in range(61, 81)],
    "imaginative_rescored": [f"adj{i}" for i in range(81, 101)],
}
for score_name, cols in cluster_map.items():
    df[score_name] = df[cols].mean(axis=1)

descriptor_summary = df[DESCRIPTORS].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "descriptor"})
cluster_summary = df[CLUSTERS + CRITERIA + DERIVED].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
correlations = df[CLUSTERS + CRITERIA + DERIVED].corr()
pca_summary, component_scores = standardized_pca_variance(df[DESCRIPTORS], n_components=12)

for idx in range(component_scores.shape[1]):
    df[f"lexical_component_{idx+1}"] = component_scores[:, idx]

reliability = pd.DataFrame([
    {"scale": "sociable_descriptor_block_adj1_adj20", "level": "descriptor_cluster", "n_items": 20, "cronbach_alpha": cronbach_alpha(df[[f"adj{i}" for i in range(1, 21)]])},
    {"scale": "reliable_descriptor_block_adj21_adj40", "level": "descriptor_cluster", "n_items": 20, "cronbach_alpha": cronbach_alpha(df[[f"adj{i}" for i in range(21, 41)]])},
    {"scale": "compassionate_descriptor_block_adj41_adj60", "level": "descriptor_cluster", "n_items": 20, "cronbach_alpha": cronbach_alpha(df[[f"adj{i}" for i in range(41, 61)]])},
    {"scale": "anxious_descriptor_block_adj61_adj80", "level": "descriptor_cluster", "n_items": 20, "cronbach_alpha": cronbach_alpha(df[[f"adj{i}" for i in range(61, 81)]])},
    {"scale": "imaginative_descriptor_block_adj81_adj100", "level": "descriptor_cluster", "n_items": 20, "cronbach_alpha": cronbach_alpha(df[[f"adj{i}" for i in range(81, 101)]])},
    {"scale": "full_lexical_descriptor_pool_adj1_adj100", "level": "full_descriptor_pool", "n_items": 100, "cronbach_alpha": cronbach_alpha(df[DESCRIPTORS])},
])

models = {
    "social_reliability_from_clusters": ols(df, "social_reliability_outcome", ["reliable_cluster_score", "compassionate_cluster_score", "anxious_cluster_score"]),
    "interpersonal_trust_from_clusters": ols(df, "interpersonal_trust_outcome", ["compassionate_cluster_score", "sociable_cluster_score", "anxious_cluster_score"]),
    "expressive_engagement_from_clusters": ols(df, "expressive_engagement_outcome", ["sociable_cluster_score", "imaginative_cluster_score", "anxious_cluster_score"]),
    "lexical_visibility_from_components": ols(df, "lexical_visibility_index", [f"lexical_component_{i}" for i in range(1, 6)]),
    "structural_centrality_from_abundance_and_redundancy": ols(df, "structural_centrality_index", ["lexical_abundance_index", "descriptor_redundancy_index", "cross_language_caution_index"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, descriptor-pool development, consulting support, organizational learning, cultural analysis, and methodological comparison; not a standalone assessment, diagnosis, placement, screening, moral-labeling, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

# Approximate five-versus-six component criterion comparison.
component_models = {
    "five_component_social_reliability": ols(df, "social_reliability_outcome", [f"lexical_component_{i}" for i in range(1, 6)]),
    "six_component_social_reliability": ols(df, "social_reliability_outcome", [f"lexical_component_{i}" for i in range(1, 7)]),
    "five_component_interpersonal_trust": ols(df, "interpersonal_trust_outcome", [f"lexical_component_{i}" for i in range(1, 6)]),
    "six_component_interpersonal_trust": ols(df, "interpersonal_trust_outcome", [f"lexical_component_{i}" for i in range(1, 7)]),
}
component_comparison = pd.DataFrame([
    {
        "comparison": "six_minus_five_components_social_reliability_r2",
        "delta_r2": component_models["six_component_social_reliability"]["r_squared"] - component_models["five_component_social_reliability"]["r_squared"],
    },
    {
        "comparison": "six_minus_five_components_interpersonal_trust_r2",
        "delta_r2": component_models["six_component_interpersonal_trust"]["r_squared"] - component_models["five_component_interpersonal_trust"]["r_squared"],
    },
])

descriptor_summary.to_csv(OUT / "python_descriptor_summary.csv", index=False)
cluster_summary.to_csv(OUT / "python_cluster_summary.csv", index=False)
correlations.to_csv(OUT / "python_lexical_cluster_correlations.csv")
pca_summary.to_csv(OUT / "python_pca_dimensionality_summary.csv", index=False)
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
component_comparison.to_csv(OUT / "python_five_six_component_comparison.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_lexical_descriptors.csv", index=False)
print(f"Wrote outputs to {OUT}")
