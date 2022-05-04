WITH potential_new_matches_array AS (
    SELECT ARRAY[{MATCH_IDS}] AS match_ids
),
potential_new_matches AS (
    SELECT
        UNNEST(match_ids) AS match_id
    FROM potential_new_matches_array
)
SELECT
    pm.match_id
FROM potential_new_matches pm
LEFT JOIN matches m
    ON m.match_id = pm.match_id
WHERE m.match_id IS NULL
;