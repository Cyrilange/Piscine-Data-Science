DELETE FROM customers c1
WHERE EXISTS (
    SELECT 1
    FROM customers c2
    WHERE c2.event_type = c1.event_type
      AND c2.product_id = c1.product_id
      AND c2.user_id = c1.user_id
      AND c2.user_session = c1.user_session
      AND c2.event_time < c1.event_time
      AND c1.event_time - c2.event_time <= INTERVAL '1 second'
);