#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_personality_twin_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

REQUIRED = {
    "pair_id",
    "zygosity",
    "genetic_relatedness",
    "twin1_trait",
    "twin2_trait",
    "twin1_temperament_reactivity",
    "twin2_temperament_reactivity",
    "twin1_effortful_control",
    "twin2_effortful_control",
    "family_stress",
    "social_support",
    "socioeconomic_security",
    "educational_stability",
    "shared_environment_index",
    "nonshared_environment_index",
    "trait_mean",
    "trait_difference",
    "gxe_marker",
    "rge_marker",
    "developmental_context_score",
}

def twin_corr(frame: pd.DataFrame, col1: str, col2: str) -> float:
    return float(frame[[col1, col2]].corr().iloc[0, 1])

def rough_ace(r_mz: float, r_dz: float) -> dict:
    return {
        "additive_genetic_h2": 2 * (r_mz - r_dz),
        "shared_environment_c2": 2 * r_dz - r_mz,
        "nonshared_environment_e2": 1 - r_mz,
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

cor_rows = []
for outcome, c1, c2 in [
    ("personality_trait", "twin1_trait", "twin2_trait"),
    ("temperament_reactivity", "twin1_temperament_reactivity", "twin2_temperament_reactivity"),
    ("effortful_control", "twin1_effortful_control", "twin2_effortful_control"),
]:
    for zygosity, group in df.groupby("zygosity"):
        cor_rows.append({
            "outcome": outcome,
            "zygosity": zygosity,
            "n_pairs": int(len(group)),
            "twin_correlation": twin_corr(group, c1, c2),
        })

correlations = pd.DataFrame(cor_rows)

ace_rows = []
for outcome in correlations["outcome"].unique():
    sub = correlations[correlations["outcome"] == outcome]
    r_mz = float(sub.loc[sub["zygosity"] == "MZ", "twin_correlation"].iloc[0])
    r_dz = float(sub.loc[sub["zygosity"] == "DZ", "twin_correlation"].iloc[0])
    estimates = rough_ace(r_mz, r_dz)
    for component, estimate in estimates.items():
        ace_rows.append({
            "outcome": outcome,
            "component": component,
            "estimate": estimate,
            "r_mz": r_mz,
            "r_dz": r_dz,
        })

ace_summary = pd.DataFrame(ace_rows)

rng = np.random.default_rng(20260522)
boot_rows = []
for replicate in range(500):
    sampled = []
    for zygosity, group in df.groupby("zygosity"):
        sampled.append(group.sample(n=len(group), replace=True, random_state=int(rng.integers(0, 1_000_000))))
    boot = pd.concat(sampled, ignore_index=True)
    r_mz = twin_corr(boot[boot["zygosity"] == "MZ"], "twin1_trait", "twin2_trait")
    r_dz = twin_corr(boot[boot["zygosity"] == "DZ"], "twin1_trait", "twin2_trait")
    est = rough_ace(r_mz, r_dz)
    boot_rows.append({"replicate": replicate + 1, **est})

bootstrap = pd.DataFrame(boot_rows)

bootstrap_summary = pd.DataFrame([
    {
        "component": component,
        "mean": float(bootstrap[component].mean()),
        "lower_95": float(bootstrap[component].quantile(0.025)),
        "upper_95": float(bootstrap[component].quantile(0.975)),
    }
    for component in ["additive_genetic_h2", "shared_environment_c2", "nonshared_environment_e2"]
])

pair_summary = (
    df.groupby("zygosity")
    .agg(
        n_pairs=("pair_id", "count"),
        trait_mean=("trait_mean", "mean"),
        trait_difference_mean=("trait_difference", "mean"),
        family_stress_mean=("family_stress", "mean"),
        social_support_mean=("social_support", "mean"),
        socioeconomic_security_mean=("socioeconomic_security", "mean"),
        nonshared_environment_mean=("nonshared_environment_index", "mean"),
        gxe_marker_mean=("gxe_marker", "mean"),
        rge_marker_mean=("rge_marker", "mean"),
        developmental_context_mean=("developmental_context_score", "mean"),
    )
    .reset_index()
)

df["zygosity_mz"] = (df["zygosity"] == "MZ").astype(int)
for variable in ["family_stress", "social_support", "socioeconomic_security", "educational_stability"]:
    df[f"{variable}_centered"] = df[variable] - df[variable].mean()

models = {
    "trait_difference_environmental_moderation": ols(
        df,
        "trait_difference",
        ["zygosity_mz", "family_stress_centered", "social_support_centered", "socioeconomic_security_centered", "nonshared_environment_index"],
    ),
    "gxe_marker_context": ols(
        df,
        "gxe_marker",
        ["genetic_relatedness", "family_stress_centered", "social_support_centered", "educational_stability_centered"],
    ),
    "rge_marker_context": ols(
        df,
        "rge_marker",
        ["trait_mean", "social_support_centered", "socioeconomic_security_centered", "developmental_context_score"],
    ),
    "professional_use_boundary": "Suitable for education, research prototyping, consulting support, organizational learning, and methodological demonstration; not a standalone genetic assessment, screening, prediction, or decision system.",
}

correlations.to_csv(OUT / "python_twin_correlations.csv", index=False)
ace_summary.to_csv(OUT / "python_rough_ace_summary.csv", index=False)
bootstrap.to_csv(OUT / "python_ace_bootstrap.csv", index=False)
bootstrap_summary.to_csv(OUT / "python_ace_bootstrap_summary.csv", index=False)
pair_summary.to_csv(OUT / "python_pair_summary.csv", index=False)
df.to_csv(OUT / "python_scored_personality_twin_data.csv", index=False)
df[
    [
        "genetic_relatedness",
        "twin1_trait",
        "twin2_trait",
        "trait_mean",
        "trait_difference",
        "family_stress",
        "social_support",
        "socioeconomic_security",
        "educational_stability",
        "shared_environment_index",
        "nonshared_environment_index",
        "gxe_marker",
        "rge_marker",
        "developmental_context_score",
    ]
].corr().to_csv(OUT / "python_behavior_genetics_correlations.csv")
(OUT / "python_models.json").write_text(json.dumps(models, indent=2))
print(f"Wrote outputs to {OUT}")
