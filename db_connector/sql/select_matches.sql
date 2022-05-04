SELECT
    match_id,
    match_type,
    total_damage,
    total_damage_with_parries_blocks,
    highest_damage,
    received_damage,
    received_attacks,
    dodged_attacks,
    partial_dodged_attacks,
    parried_attacks,
    blocked_attacks,
    partial_blocked_attacks,
    missed_attacks,
    partial_missed_attacks
FROM matches
ORDER BY match_id DESC
LIMIT {MAX_NR_MATCHES}