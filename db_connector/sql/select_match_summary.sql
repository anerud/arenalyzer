SELECT
    m.match_id,
    m.match_type,
    m.match_tactic,
    ms.gladiator_name,
    ms.total_damage,
    ms.total_damage_with_parries_blocks,
    ms.highest_damage,
    ms.received_damage,
    ms.received_attacks,
    ms.dodged_attacks,
    ms.partial_dodged_attacks,
    ms.parried_attacks,
    ms.blocked_attacks,
    ms.partial_blocked_attacks,
    ms.missed_attacks,
    ms.partial_missed_attacks
FROM match_summary ms
INNER JOIN match m ON m.match_id = ms.match_id
WHERE ms.gladiator_name = '{GLADIATOR_NAME}'
ORDER BY m.match_id DESC
LIMIT {MAX_NR_MATCHES}