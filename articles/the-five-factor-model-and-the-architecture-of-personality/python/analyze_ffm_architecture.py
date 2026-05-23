#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_ffm_items.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

DOMAINS = ["extraversion_score", "agreeableness_score", "conscientiousness_score", "neuroticism_score", "openness_score"]
FACETS = [
    "sociability_score", "assertiveness_score", "compassion_score", "politeness_score",
    "orderliness_score", "industriousness_score", "anxiety_score", "volatility_score",
    "aesthetics_score", "intellect_score"
]
OUTCOMES = ["outcome_score", "broad_life_functioning", "relationship_functioning", "creative_engagement", "emotional_distress"]
DERIVED = ["facet_profile_dispersion", "hierarchy_consistency_index", "bandwidth_fidelity_gap", "domain_facet_alignment"]
ITEMS = [f"item{i}" for i in range(1, 61)]
REQUIRED = {"respondent_id", *ITEMS, "c1", "c2", "c3", "c4", "c5", "c6", "o1", "o2", "o3", "i1", "i2", "i3", *DOMAINS, *FACETS, *OUTCOMES, *DERIVED}

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

def standardized_pca_variance(frame: pd.DataFrame, n_components: int = 10) -> pd.DataFrame:
    X = frame.to_numpy(float)
    X = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    cov = np.cov(X, rowvar=False)
    eigvals = np.linalg.eigvalsh(cov)[::-1]
    ratios = eigvals / eigvals.sum()
    return pd.DataFrame({
        "component": list(range(1, n_components + 1)),
        "explained_variance_ratio": ratios[:n_components],
        "cumulative_explained_variance": np.cumsum(ratios[:n_components]),
    })

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

# Re-score example domain and facets from item subsets.
df["conscientiousness_rescored"] = df[["c1", "c2", "c3", "c4", "c5", "c6"]].mean(axis=1)
df["orderliness_rescored"] = df[["o1", "o2", "o3"]].mean(axis=1)
df["industriousness_rescored"] = df[["i1", "i2", "i3"]].mean(axis=1)

domain_summary = df[DOMAINS + OUTCOMES + DERIVED].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
facet_summary = df[FACETS + OUTCOMES + DERIVED].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
correlations = df[DOMAINS + FACETS + OUTCOMES + DERIVED].corr()
pca_summary = standardized_pca_variance(df[ITEMS], n_components=10)

reliability = pd.DataFrame([
    {"scale": "full_item_pool_item1_item60", "level": "broad_item_pool", "n_items": 60, "cronbach_alpha": cronbach_alpha(df[ITEMS])},
    {"scale": "conscientiousness_c1_c6", "level": "domain_item_set", "n_items": 6, "cronbach_alpha": cronbach_alpha(df[["c1", "c2", "c3", "c4", "c5", "c6"]])},
    {"scale": "orderliness_o1_o3", "level": "facet_item_set", "n_items": 3, "cronbach_alpha": cronbach_alpha(df[["o1", "o2", "o3"]])},
    {"scale": "industriousness_i1_i3", "level": "facet_item_set", "n_items": 3, "cronbach_alpha": cronbach_alpha(df[["i1", "i2", "i3"]])},
])

models = {
    "broad_life_functioning_from_domains": ols(df, "broad_life_functioning", DOMAINS),
    "relationship_functioning_from_social_domains": ols(df, "relationship_functioning", ["extraversion_score", "agreeableness_score", "sociability_score", "compassion_score"]),
    "creative_engagement_from_openness": ols(df, "creative_engagement", ["openness_score", "aesthetics_score", "intellect_score"]),
    "emotional_distress_from_neuroticism": ols(df, "emotional_distress", ["neuroticism_score", "anxiety_score", "volatility_score"]),
    "outcome_from_conscientiousness_domain": ols(df, "outcome_score", ["conscientiousness_score"]),
    "outcome_from_conscientiousness_facets": ols(df, "outcome_score", ["orderliness_score", "industriousness_score"]),
    "facet_to_domain_hierarchy": ols(df, "conscientiousness_score", ["orderliness_score", "industriousness_score"]),
    "bandwidth_fidelity_gap_from_profile_structure": ols(df, "bandwidth_fidelity_gap", ["facet_profile_dispersion", "hierarchy_consistency_index", "domain_facet_alignment"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, consulting support, organizational learning, coaching reflection, and methodological comparison; not a standalone assessment, diagnosis, placement, screening, moral-labeling, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

comparison = pd.DataFrame([
    {
        "comparison": "facet_minus_domain_prediction_r2_for_outcome_score",
        "delta_r2": models["outcome_from_conscientiousness_facets"]["r_squared"] - models["outcome_from_conscientiousness_domain"]["r_squared"],
    },
    {
        "comparison": "hierarchy_model_r2_conscientiousness_from_facets",
        "delta_r2": models["facet_to_domain_hierarchy"]["r_squared"],
    },
])

domain_summary.to_csv(OUT / "python_domain_summary.csv", index=False)
facet_summary.to_csv(OUT / "python_facet_summary.csv", index=False)
correlations.to_csv(OUT / "python_ffm_correlations.csv")
pca_summary.to_csv(OUT / "python_pca_dimensionality_summary.csv", index=False)
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
comparison.to_csv(OUT / "python_domain_facet_comparison.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_ffm_items.csv", index=False)
print(f"Wrote outputs to {OUT}")
