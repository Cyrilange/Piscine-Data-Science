
DROP TABLE IF EXISTS customers_fused;

CREATE TABLE customers_mix AS
SELECT
    c.event_time,
    c.event_type,
    c.product_id,
    c.price,
    c.user_id,
    c.user_session,
    i.category_id,
    i.category_code,
    i.brand
FROM customers AS c
LEFT JOIN (
    SELECT DISTINCT ON (product_id)
        product_id,
        category_id,
        category_code,
        brand
    FROM items
    ORDER BY
        product_id,
        category_id DESC NULLS LAST,
        category_code DESC NULLS LAST,
        brand DESC NULLS LAST
) AS i
    ON c.product_id = i.product_id;

DROP TABLE customers;

ALTER TABLE customers_mix RENAME TO customers;
