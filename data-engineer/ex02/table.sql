CREATE TABLE data_2022_oct (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type TEXT,
    product_id INTEGER,
    price NUMERIC,
    user_id BIGINT,
    user_session UUID
);


-- psql -U csalamit -d piscineds -h localhost -W -c "\copy data_2022_oct FROM 'customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true, NULL '')"

-- check:
-- SELECT COUNT(*) FROM data_2022_oct;
-- SELECT * FROM data_2022_oct LIMIT 5;
-- SELECT COUNT(*) FROM data_2022_oct WHERE user_session IS NULL;