import psycopg2


connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="csalamit",
    password="mysecretpassword",
    dbname="piscineds"
)

cursor = connection.cursor()

cursor.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = 'customers'
    )
""")

table_exists = cursor.fetchone()[0]

if table_exists:
    print("=== EX01 : CUSTOMERS TABLE ===")
    print("Table customers already exists.")

else:
    print("=== EX01 : CUSTOMERS TABLE ===")
    print("Creating customers table...")

    with open("customers_table.sql", "r") as sql_file:
        cursor.execute(sql_file.read())

    connection.commit()

    print("Table customers created.")

cursor.execute("""
    SELECT COUNT(*)
    FROM customers
""")

total_rows = cursor.fetchone()[0]

cursor.execute("""
    SELECT MIN(event_time), MAX(event_time)
    FROM customers
""")

first_event, last_event = cursor.fetchone()

cursor.execute("""
    SELECT COUNT(DISTINCT user_id)
    FROM customers
    WHERE user_id IS NOT NULL
""")

unique_users = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(DISTINCT product_id)
    FROM customers
    WHERE product_id IS NOT NULL
""")

unique_products = cursor.fetchone()[0]

print()
print("Customers table information:")
print(f"Rows: {total_rows}")
print(f"First event: {first_event}")
print(f"Last event: {last_event}")
print(f"Unique users: {unique_users}")
print(f"Unique products: {unique_products}")

cursor.close()
connection.close()