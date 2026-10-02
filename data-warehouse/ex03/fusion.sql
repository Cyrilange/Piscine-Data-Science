ALTER TABLE customers
ADD COLUMN IF NOT EXISTS category_id BIGINT,
ADD COLUMN IF NOT EXISTS category_code TEXT,
ADD COLUMN IF NOT EXISTS brand VARCHAR(255);

UPDATE customers
SET
    category_id = NULL,
    category_code = NULL,
    brand = NULL;

UPDATE customers c
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM items i
WHERE c.product_id = i.product_id;