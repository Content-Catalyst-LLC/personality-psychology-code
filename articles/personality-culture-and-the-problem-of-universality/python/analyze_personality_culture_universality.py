#!/usr/bin/env python3
"""Analyze synthetic cross-cultural personality data.

This script supports the article "Personality, Culture, and the Problem of Universality."
It demonstrates group summaries, within-group correlation matrices, and matrix-similarity
comparisons using synthetic data only.
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_culture_universality.csv"
OUTPUTS = ROOT / "outputs"

TRAITS = [
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
    "honesty_humility",
]


def upper_triangle_values(matrix: pd.DataFrame) -> pd.Series:
    """Return upper-triangle values from a square correlation matrix."""
    mask = np.triu(np.ones(matrix.shape), k=1).astype(bool)
    return matrix.where(mask).stack()


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    required = {"participant_id", "culture_group", *TRAITS, "context_collectivism", "behavioral_manifestation"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    group_summary = (
        df.groupby("culture_group")
        .agg(
            n=("participant_id", "count"),
            openness_mean=("openness", "mean"),
            conscientiousness_mean=("conscientiousness", "mean"),
            extraversion_mean=("extraversion", "mean"),
            agreeableness_mean=("agreeableness", "mean"),
            neuroticism_mean=("neuroticism", "mean"),
            honesty_humility_mean=("honesty_humility", "mean"),
            context_collectivism_mean=("context_collectivism", "mean"),
            behavioral_manifestation_mean=("behavioral_manifestation", "mean"),
        )
        .reset_index()
    )

    group_summary.to_csv(OUTPUTS / "python_group_summary.csv", index=False)

    pooled_corr = df[TRAITS].corr()
    pooled_corr.to_csv(OUTPUTS / "python_pooled_trait_correlations.csv")

    pooled_values = upper_triangle_values(pooled_corr)

    rows = []
    for group, group_df in df.groupby("culture_group"):
        corr = group_df[TRAITS].corr()
        corr.to_csv(OUTPUTS / f"python_correlations_{group}.csv")

        group_values = upper_triangle_values(corr)
        aligned = pd.concat([pooled_values, group_values], axis=1).dropna()
        aligned.columns = ["pooled", "group"]

        similarity = aligned["pooled"].corr(aligned["group"])
        rows.append(
            {
                "culture_group": group,
                "matrix_similarity_with_pooled": round(float(similarity), 4),
                "n": int(len(group_df)),
            }
        )

    replicability = pd.DataFrame(rows)
    replicability.to_csv(OUTPUTS / "python_matrix_similarity.csv", index=False)

    # Simple trait-context behavioral model using numpy least squares.
    # behavioral_manifestation ~ conscientiousness + agreeableness + honesty_humility + context_collectivism
    X = df[["conscientiousness", "agreeableness", "honesty_humility", "context_collectivism"]].to_numpy()
    X = np.column_stack([np.ones(len(X)), X])
    y = df["behavioral_manifestation"].to_numpy()
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)

    model = {
        "intercept": float(beta[0]),
        "conscientiousness": float(beta[1]),
        "agreeableness": float(beta[2]),
        "honesty_humility": float(beta[3]),
        "context_collectivism": float(beta[4]),
        "note": "Synthetic demonstration only; not a real psychological model.",
    }

    with open(OUTPUTS / "python_behavioral_model.json", "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)

    print("Wrote Python outputs to:", OUTPUTS)


if __name__ == "__main__":
    main()
