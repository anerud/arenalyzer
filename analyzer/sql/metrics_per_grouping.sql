SELECT
    {GROUPING},
    COUNT(...) AS nr_xxx,
    AVG(...)   AS avg_xxx,
    MAX(...)   AS max_xxx
FROM matches
WHERE gladiator_name = '{GLADIATOR_NAME}'
    AND gladiator_level BETWEEN {MIN_LEVEL} AND {MAX_LEVEL}
GROUP BY {GROUPING}
ORDER BY {GROUPING}
;