-- Article-level synthetic personality psychology schema.

CREATE TABLE IF NOT EXISTS personality_trait_scores (
    score_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    period INTEGER NOT NULL,
    trait_name TEXT NOT NULL,
    facet_name TEXT,
    score_value REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS personality_outcomes (
    outcome_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    period INTEGER NOT NULL,
    identity_integration REAL,
    self_regulation REAL,
    adaptive_flexibility REAL,
    maladaptive_pressure REAL,
    personality_organization REAL
);

CREATE INDEX IF NOT EXISTS idx_trait_scores_participant
ON personality_trait_scores(participant_id);

CREATE INDEX IF NOT EXISTS idx_trait_scores_trait
ON personality_trait_scores(trait_name);

CREATE INDEX IF NOT EXISTS idx_personality_outcomes_period
ON personality_outcomes(period);
