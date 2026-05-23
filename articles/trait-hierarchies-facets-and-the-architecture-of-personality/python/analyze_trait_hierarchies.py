#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_hierarchical_trait_items.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

DOMAINS = ["extraversion_score", "agreeableness_score", "conscientiousness_score", "neuroticism_score", "openness_score"]
FACETS = [
    "sociability_score", "assertiveness_score", "compassion_score", "politeness_score",
    "orderliness_score", "industriousness_score", "anxiety_score", "volatility_score",
    "aesthetics_score", "intellect_score"
]
OUTCOMES = ["broad_life_functioning", "focused_reliability_outcome", "creative_engagement_outcome"]
DERIVED = ["bandwidth_fidelity_gap", "facet_profile_dispersion", "hierarchy_consistency_index"]

REQUIRED = {"respondent_id", *[f"item{i}" for i in range(1, 61)], "c1", "c2", "c3", "c4", "c5", "c6", "o1", "o2", "o3", "i1", "i2", "i3", *DOMAINS, *FACETS, *OUTCOMES, *DERIVED}

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

df = pd.read_csv(DATA)
missing = REQUIRED - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

# Re-score key domain and facet examples from item columns.
df["conscientiousness_rescored"] = df[["c1", "c2", "c3", "c4", "c5", "c6"]].mean(axis=1)
df["orderliness_rescored"] = df[["o1", "o2", "o3"]].mean(axis=1)
df["industriousness_rescored"] = df[["i1", "i2", "i3"]].mean(axis=1)

reliability = pd.DataFrame([
    {"scale": "conscientiousness_c1_c6", "level": "domain_item_set", "n_items": 6, "cronbach_alpha": cronbach_alpha(df[["c1", "c2", "c3", "c4", "c5", "c6"]])},
    {"scale": "orderliness_o1_o3", "level": "facet_item_set", "n_items": 3, "cronbach_alpha": cronbach_alpha(df[["o1", "o2", "o3"]])},
    {"scale": "industriousness_i1_i3", "level": "facet_item_set", "n_items": 3, "cronbach_alpha": cronbach_alpha(df[["i1", "i2", "i3"]])},
    {"scale": "broad_item_pool_item1_item60", "level": "broad_item_pool", "n_items": 60, "cronbach_alpha": cronbach_alpha(df[[f"item{i}" for i in range(1, 61)]])},
])

domain_summary = df[DOMAINS + OUTCOMES + DERIVED].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
facet_summary = df[FACETS + OUTCOMES + DERIVED].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
correlations = df[DOMAINS + FACETS + OUTCOMES + DERIVED].corr()

models = {
    "broad_life_functioning_from_domains": ols(df, "broad_life_functioning", DOMAINS),
    "focused_reliability_from_conscientiousness_domain": ols(df, "focused_reliability_outcome", ["conscientiousness_score"]),
    "focused_reliability_from_conscientiousness_facets": ols(df, "focused_reliability_outcome", ["orderliness_score", "industriousness_score"]),
    "creative_engagement_from_openness_domain": ols(df, "creative_engagement_outcome", ["openness_score"]),
    "creative_engagement_from_openness_facets": ols(df, "creative_engagement_outcome", ["aesthetics_score", "intellect_score"]),
    "bandwidth_fidelity_gap_from_profile_dispersion": ols(df, "bandwidth_fidelity_gap", ["facet_profile_dispersion", "hierarchy_consistency_index"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, consulting support, organizational learning, coaching reflection, and methodological comparison; not a standalone assessment, diagnosis, placement, screening, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

domain_summary.to_csv(OUT / "python_domain_summary.csv", index=False)
facet_summary.to_csv(OUT / "python_facet_summary.csv", index=False)
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
correlations.to_csv(OUT / "python_trait_hierarchy_correlations.csv")
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_hierarchical_trait_items.csv", index=False)
print(f"Wrote outputs to {OUT}")
