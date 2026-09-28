import os
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="csalamit",
    password="mysecretpassword",
    dbname="piscineds"
)

cursor = connection.cursor()

customer_dir = "subject/customer"

for filename in sorted(os.listdir(customer_dir)):
    if filename.endswith(".csv"):
        table_name = os.path.splitext(filename)[0]

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            )
        """, (table_name,))

        table_exists = cursor.fetchone()[0]

        if table_exists:
            print(f"{table_name}: already exists, skipped")
            continue

        cursor.execute(f"""
            CREATE TABLE {table_name} (
                event_time TIMESTAMP WITH TIME ZONE,
                event_type TEXT,
                product_id BIGINT,
                price NUMERIC,
                user_id BIGINT,
                user_session UUID
            )
        """)

        with open(os.path.join(customer_dir, filename), "r") as csv_file:
            cursor.copy_expert(
                f"COPY {table_name} FROM STDIN WITH (FORMAT csv, HEADER true, NULL '')",
                csv_file
            )

        print(f"{table_name}: created and imported")

connection.commit()

cursor.close()
connection.close()

# to check:

# psql -U csalamit -d piscineds -h localhost -W -c "
# SELECT
#     'data_2022_dec' AS table_name, COUNT(*) FROM data_2022_dec
# UNION ALL
# SELECT
#     'data_2022_nov', COUNT(*) FROM data_2022_nov
# UNION ALL
# SELECT
#     'data_2022_oct', COUNT(*) FROM data_2022_oct
# UNION ALL
# SELECT
#     'data_2023_jan', COUNT(*) FROM data_2023_jan;
# "