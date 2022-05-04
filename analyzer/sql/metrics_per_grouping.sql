WITH last_x_matches AS (
    SELECT
        *,
        ROW_NUMBER() OVER(ORDER BY match_id DESC) AS match_rank
    FROM matches
    WHERE gladiator_name = '{GLADIATOR_NAME}'
        AND gladiator_level BETWEEN {MIN_LEVEL} AND {MAX_LEVEL}
)
SELECT
    {GROUPING},
    COUNT(...) AS nr_xxx,
    AVG(...)   AS avg_xxx,
    MAX(...)   AS max_xxx
FROM last_x_matches
WHERE match_rank <= {MATCH_LIMIT}
GROUP BY {GROUPING}
ORDER BY {GROUPING}
;