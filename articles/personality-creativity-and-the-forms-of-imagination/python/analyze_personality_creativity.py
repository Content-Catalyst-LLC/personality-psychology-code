#!/usr/bin/env python3
"""Analyze synthetic personality-creativity data.

This script demonstrates a transparent companion workflow for the article
"Personality, Creativity, and the Forms of Imagination."

Outputs are written to outputs/tables and outputs/figures.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ARTICLE_DIR / "data" / "synthetic_personality_creativity.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
FIGURE_DIR = ARTICLE_DIR / "outputs" / "figures"


def ensure_output_dirs() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    required = {
        "participant_id",
        "domain",
        "openness",
        "intellect",
        "conscientiousness",
        "extraversion",
        "agreeableness",
        "neuroticism",
        "persistence",
        "social_support",
        "divergent_thinking",
        "creative_achievement",
        "everyday_creativity",
    }
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def write_descriptive_outputs(df: pd.DataFrame) -> None:
    numeric_cols = [
        "openness",
        "intellect",
        "conscientiousness",
        "extraversion",
        "agreeableness",
        "neuroticism",
        "persistence",
        "social_support",
        "divergent_thinking",
        "creative_achievement",
        "everyday_creativity",
    ]

    desc = df[numeric_cols].describe().T
    desc.to_csv(TABLE_DIR / "python_descriptive_statistics.csv")

    corr = df[numeric_cols].corr(numeric_only=True)
    corr.to_csv(TABLE_DIR / "python_correlation_matrix.csv")


def fit_models(df: pd.DataFrame) -> pd.DataFrame:
    formulas = {
        "divergent_thinking": (
            "divergent_thinking ~ openness + intellect + conscientiousness + "
            "extraversion + agreeableness + neuroticism"
        ),
        "creative_achievement": (
            "creative_achievement ~ openness + intellect + conscientiousness + "
            "persistence + social_support + C(domain)"
        ),
        "everyday_creativity": (
            "everyday_creativity ~ openness + intellect + conscientiousness + "
            "extraversion + agreeableness + persistence + social_support + C(domain)"
        ),
    }

    rows = []
    for model_name, formula in formulas.items():
        model = smf.ols(formula=formula, data=df).fit()
        for term, coef, pvalue in zip(model.params.index, model.params.values, model.pvalues.values):
            rows.append(
                {
                    "model": model_name,
                    "term": term,
                    "coefficient": coef,
                    "p_value": pvalue,
                    "r_squared": model.rsquared,
                    "n": int(model.nobs),
                }
            )

    results = pd.DataFrame(rows)
    results.to_csv(TABLE_DIR / "python_model_coefficients.csv", index=False)
    return results


def plot_relationship(df: pd.DataFrame, x_col: str, y_col: str, file_name: str) -> None:
    x = df[x_col].to_numpy()
    y = df[y_col].to_numpy()

    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, alpha=0.75)

    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line)

    plt.title(f"{x_col.replace('_', ' ').title()} and {y_col.replace('_', ' ').title()}")
    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel(y_col.replace("_", " ").title())
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / file_name, dpi=300)
    plt.close()


def main() -> None:
    ensure_output_dirs()
    df = load_data()

    write_descriptive_outputs(df)
    fit_models(df)

    plot_relationship(
        df,
        "openness",
        "divergent_thinking",
        "python_openness_divergent_thinking.png",
    )
    plot_relationship(
        df,
        "openness",
        "creative_achievement",
        "python_openness_creative_achievement.png",
    )

    print("Python analysis complete.")
    print(f"Tables written to: {TABLE_DIR}")
    print(f"Figures written to: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
