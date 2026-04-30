-- Root schema for personality psychology assessment, traits, and longitudinal data.

CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    age_years REAL,
    birth_cohort INTEGER,
    language_background TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS inventories (
    inventory_id TEXT PRIMARY KEY,
    inventory_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS trait_scores (
    score_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    inventory_id TEXT NOT NULL,
    wave INTEGER,
    trait_name TEXT NOT NULL,
    facet_name TEXT,
    score_value REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS personality_outcomes (
    outcome_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    wave INTEGER,
    self_regulation REAL,
    identity_integration REAL,
    adaptive_flexibility REAL,
    maladaptive_pressure REAL,
    wellbeing_score REAL,
    leadership_fit REAL,
    health_behavior_score REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
