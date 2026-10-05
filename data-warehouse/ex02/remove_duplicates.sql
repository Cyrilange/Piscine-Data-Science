
DELETE FROM customers AS c
USING (
    SELECT s.ctid AS rid
    FROM (
        SELECT
            ctid,
            event_time,
            LAG(event_time) OVER (
                PARTITION BY
                    user_id,
                    user_session,
                    event_type,
                    product_id,
                    price
                ORDER BY
                    event_time,
                    ctid
            ) AS prev_time
        FROM customers
    ) AS s
    WHERE s.prev_time IS NOT NULL
      AND s.event_time - s.prev_time <= INTERVAL '1 second'
) AS d
WHERE c.ctid = d.rid;