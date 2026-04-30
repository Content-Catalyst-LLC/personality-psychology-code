"""Synthetic personality psychology simulation.

This script creates toy longitudinal personality data for article examples.
It is educational only and not a clinical, diagnostic, hiring, or assessment tool.
"""

from pathlib import Path
import csv
import random

random.seed(42)

n_people = 220
n_periods = 12

traits = [
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
    "honesty_humility"
]

rows = []
outcome_rows = []
score_id = 1
outcome_id = 1

for person_index in range(1, n_people + 1):
    participant = f"P{person_index:03d}"

    trait_values = {
        trait: random.uniform(0.20, 0.90)
        for trait in traits
    }

    identity_integration = random.uniform(0.25, 0.90)
    self_regulation = random.uniform(0.25, 0.90)
    adaptive_flexibility = random.uniform(0.25, 0.90)
    maladaptive_pressure = random.uniform(0.05, 0.80)

    for period in range(1, n_periods + 1):
        stress = random.uniform(0.0, 0.45)

        for trait, value in trait_values.items():
            drift = random.gauss(0.0, 0.025)
            if trait == "conscientiousness":
                drift += 0.010
            if trait == "neuroticism":
                drift += stress * 0.025

            trait_values[trait] = max(0.0, min(1.0, value + drift))

            rows.append({
                "score_id": score_id,
                "participant": participant,
                "period": period,
                "trait_name": trait,
                "score_value": round(trait_values[trait], 3),
            })
            score_id += 1

        personality_organization = (
            0.18 * trait_values["conscientiousness"] +
            0.15 * trait_values["agreeableness"] +
            0.14 * trait_values["openness"] +
            0.18 * self_regulation +
            0.16 * identity_integration +
            0.14 * adaptive_flexibility -
            0.18 * maladaptive_pressure -
            0.08 * trait_values["neuroticism"]
        )

        personality_organization = max(0.0, min(1.0, personality_organization))

        outcome_rows.append({
            "outcome_id": outcome_id,
            "participant": participant,
            "period": period,
            "identity_integration": round(identity_integration, 3),
            "self_regulation": round(self_regulation, 3),
            "adaptive_flexibility": round(adaptive_flexibility, 3),
            "maladaptive_pressure": round(maladaptive_pressure, 3),
            "personality_organization": round(personality_organization, 3),
        })
        outcome_id += 1

        identity_integration = max(0.0, min(1.0, identity_integration + 0.02 * (personality_organization - 0.4)))
        self_regulation = max(0.0, min(1.0, self_regulation + 0.02 * (personality_organization - 0.4)))
        adaptive_flexibility = max(0.0, min(1.0, adaptive_flexibility + 0.015 * (personality_organization - 0.4)))
        maladaptive_pressure = max(0.0, min(1.0, maladaptive_pressure - 0.012 * personality_organization + stress * 0.01))

processed = Path(__file__).resolve().parents[1] / "data" / "processed"
processed.mkdir(parents=True, exist_ok=True)

scores_path = processed / "synthetic_trait_scores.csv"
outcomes_path = processed / "synthetic_personality_outcomes.csv"

with scores_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

with outcomes_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=outcome_rows[0].keys())
    writer.writeheader()
    writer.writerows(outcome_rows)

print(f"Wrote {len(rows)} trait scores to {scores_path}")
print(f"Wrote {len(outcome_rows)} personality outcomes to {outcomes_path}")
