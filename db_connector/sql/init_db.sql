CREATE TABLE IF NOT EXISTS matches(
    match_id SERIAL PRIMARY KEY,
    gladiator_name TEXT,
    match_type TEXT,
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