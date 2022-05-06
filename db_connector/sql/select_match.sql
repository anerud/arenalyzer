SELECT
    match_id,
    match_type,
    match_tactic
FROM match
WHERE gladiator_name = '{GLADIATOR_NAME}'
ORDER BY match_id DESC
LIMIT {MAX_NR_MATCHES}