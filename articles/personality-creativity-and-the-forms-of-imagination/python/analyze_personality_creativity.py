#!/usr/bin/env python3
"""Analyze synthetic personality-creativity data.

This script creates descriptive summaries, correlations, simple OLS models,
and scatter plots for the article scaffold. It uses synthetic data only.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_personality_creativity.csv"
TABLE_DIR = ROOT / "outputs" / "tables"
FIGURE_DIR = ROOT / "outputs" / "figures"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    df = pd.read_csv(DATA_PATH)

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

    df[numeric_cols].describe().round(2).to_csv(TABLE_DIR / "python_descriptive_statistics.csv")
    df[numeric_cols].corr().round(3).to_csv(TABLE_DIR / "python_correlation_matrix.csv")
    df.groupby("domain")[numeric_cols[-3:]].mean().round(2).to_csv(TABLE_DIR / "python_domain_outcome_means.csv")

    try:
        import statsmodels.formula.api as smf

        model_dt = smf.ols(
            "divergent_thinking ~ openness + intellect + conscientiousness + persistence + social_support",
            data=df,
        ).fit()
        model_ca = smf.ols(
            "creative_achievement ~ openness + intellect + conscientiousness + persistence + social_support",
            data=df,
        ).fit()
        model_domain = smf.ols(
            "creative_achievement ~ openness * C(domain) + intellect * C(domain) + persistence + social_support",
            data=df,
        ).fit()

        (TABLE_DIR / "python_model_divergent_thinking.txt").write_text(model_dt.summary().as_text())
        (TABLE_DIR / "python_model_creative_achievement.txt").write_text(model_ca.summary().as_text())
        (TABLE_DIR / "python_model_domain_sensitive.txt").write_text(model_domain.summary().as_text())
    except Exception as exc:
        (TABLE_DIR / "python_model_notes.txt").write_text(
            f"statsmodels model fitting was skipped: {exc}\n"
        )

    try:
        import matplotlib.pyplot as plt

        for x, y, name in [
            ("openness", "divergent_thinking", "openness_divergent_thinking"),
            ("openness", "creative_achievement", "openness_creative_achievement"),
            ("persistence", "creative_achievement", "persistence_creative_achievement"),
        ]:
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.scatter(df[x], df[y], alpha=0.75)
            ax.set_xlabel(x.replace("_", " ").title())
            ax.set_ylabel(y.replace("_", " ").title())
            ax.set_title(f"{x.replace('_', ' ').title()} and {y.replace('_', ' ').title()}")
            fig.tight_layout()
            fig.savefig(FIGURE_DIR / f"{name}.png", dpi=300)
            plt.close(fig)
    except Exception as exc:
        (TABLE_DIR / "python_plot_notes.txt").write_text(f"plotting was skipped: {exc}\n")

    print(f"Analysis complete. Outputs written to {TABLE_DIR} and {FIGURE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
