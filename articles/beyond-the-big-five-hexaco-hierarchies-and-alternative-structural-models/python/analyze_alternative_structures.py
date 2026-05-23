#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_alternative_structure_items.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

BF = ["bf_extraversion", "bf_agreeableness", "bf_conscientiousness", "bf_neuroticism", "bf_openness"]
HX = ["hx_honesty_humility", "hx_emotionality", "hx_extraversion", "hx_agreeableness", "hx_conscientiousness", "hx_openness"]
FACETS = [
    "sincerity_facet", "fairness_facet", "greed_avoidance_facet", "modesty_facet",
    "patience_facet", "forgiveness_facet", "anxiety_facet", "sentimentality_facet"
]
OUTCOMES = ["outcome_integrity", "outcome_interpersonal_trust", "outcome_broad_functioning", "outcome_exploitative_risk"]
DERIVED = ["hexaco_increment_marker", "repartitioning_gap", "structural_comparison_index", "facet_granularity_index"]
ITEMS = [f"item{i}" for i in range(1, 73)]
REQUIRED = {"respondent_id", *ITEMS, *BF, *HX, *FACETS, *OUTCOMES, *DERIVED}

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
    return {
        "coefficients": dict(zip(["intercept", *xs], map(float, beta))),
        "r_squared": r2,
        "n": int(len(model_df)),
    }

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

summary = df[BF + HX + FACETS + OUTCOMES + DERIVED].agg(["mean", "std", "min", "max"]).T.reset_index().rename(columns={"index": "variable"})
correlations = df[BF + HX + FACETS + OUTCOMES + DERIVED].corr()
pca_summary = standardized_pca_variance(df[ITEMS], n_components=12)

reliability = pd.DataFrame([
    {"scale": "big_five_proxy_items_1_60", "level": "five_factor_proxy_pool", "n_items": 60, "cronbach_alpha": cronbach_alpha(df[[f"item{i}" for i in range(1, 61)]])},
    {"scale": "hexaco_proxy_items_1_72", "level": "six_factor_proxy_pool", "n_items": 72, "cronbach_alpha": cronbach_alpha(df[ITEMS])},
    {"scale": "honesty_humility_facets", "level": "hexaco_domain_facets", "n_items": 4, "cronbach_alpha": cronbach_alpha(df[["sincerity_facet", "fairness_facet", "greed_avoidance_facet", "modesty_facet"]])},
    {"scale": "emotionality_agreeableness_repartition", "level": "repartitioning_facets", "n_items": 4, "cronbach_alpha": cronbach_alpha(df[["patience_facet", "forgiveness_facet", "anxiety_facet", "sentimentality_facet"]])},
])

models = {
    "integrity_from_big_five": ols(df, "outcome_integrity", BF),
    "integrity_from_hexaco": ols(df, "outcome_integrity", HX),
    "exploitative_risk_from_big_five": ols(df, "outcome_exploitative_risk", BF),
    "exploitative_risk_from_hexaco": ols(df, "outcome_exploitative_risk", HX),
    "interpersonal_trust_from_repartitioned_facets": ols(df, "outcome_interpersonal_trust", ["hx_honesty_humility", "hx_agreeableness", "hx_emotionality", "patience_facet", "forgiveness_facet"]),
    "broad_functioning_from_big_five": ols(df, "outcome_broad_functioning", BF),
    "broad_functioning_from_hexaco": ols(df, "outcome_broad_functioning", HX),
    "hexaco_increment_marker": ols(df, "hexaco_increment_marker", ["hx_honesty_humility", "outcome_integrity", "outcome_exploitative_risk", "repartitioning_gap"]),
    "professional_use_boundary": "Suitable for education, research prototyping, psychometric demonstration, consulting support, organizational learning, coaching reflection, and structural-model comparison; not a standalone assessment, diagnosis, placement, screening, moral-labeling, prediction, or decision system.",
}

model_fit = pd.DataFrame([
    {"model": name, "r_squared": spec["r_squared"], "n": spec["n"]}
    for name, spec in models.items()
    if isinstance(spec, dict)
])

comparison = pd.DataFrame([
    {
        "comparison": "integrity_hexaco_minus_big_five_r2",
        "delta_r2": models["integrity_from_hexaco"]["r_squared"] - models["integrity_from_big_five"]["r_squared"],
    },
    {
        "comparison": "exploitative_risk_hexaco_minus_big_five_r2",
        "delta_r2": models["exploitative_risk_from_hexaco"]["r_squared"] - models["exploitative_risk_from_big_five"]["r_squared"],
    },
    {
        "comparison": "broad_functioning_hexaco_minus_big_five_r2",
        "delta_r2": models["broad_functioning_from_hexaco"]["r_squared"] - models["broad_functioning_from_big_five"]["r_squared"],
    },
])

summary.to_csv(OUT / "python_alternative_structure_summary.csv", index=False)
correlations.to_csv(OUT / "python_alternative_structure_correlations.csv")
pca_summary.to_csv(OUT / "python_pca_dimensionality_summary.csv", index=False)
reliability.to_csv(OUT / "python_reliability_summary.csv", index=False)
model_fit.to_csv(OUT / "python_model_fit_summary.csv", index=False)
comparison.to_csv(OUT / "python_model_comparison_delta_r2.csv", index=False)
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
df.to_csv(OUT / "python_scored_alternative_structure_items.csv", index=False)
print(f"Wrote outputs to {OUT}")
