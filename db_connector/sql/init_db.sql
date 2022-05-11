CREATE TABLE IF NOT EXISTS match(
    id SERIAL PRIMARY KEY,
    match_id INT,
    match_type TEXT,
    match_tactic TEXT,
    gladiator_name TEXT[]
);

CREATE TABLE IF NOT EXISTS match_summary(
    id SERIAL PRIMARY KEY,
    match_id INT,
    gladiator_name TEXT,
--    gladiator_level INT,
    total_damage INT,
    total_damage_with_parries_blocks INT,
    highest_damage INT,
    received_damage INT,
    received_attacks INT,
    dodged_attacks INT,
    partial_dodged_attacks INT,
    parried_attacks INT,
    blocked_attacks INT,
    partial_blocked_attacks INT,
    missed_attacks INT,
    partial_missed_attacks INT
);

CREATE TABLE IF NOT EXISTS round(
    id SERIAL PRIMARY KEY,
    match_id INT,
    gladiator_name TEXT,
    round INT
);