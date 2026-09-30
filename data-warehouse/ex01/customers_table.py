import psycopg2


def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )
    return conn


def connect_and_load():
    conn = connect_db()
    cursor = conn.cursor()

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

        with open("customers_table.sql", "r", encoding="utf-8") as sql_file:
            cursor.execute(sql_file.read())

        conn.commit()

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

    cursor.close()
    conn.close()

    return total_rows, first_event, last_event, unique_users, unique_products


def print_all(total_rows, first_event, last_event, unique_users, unique_products):
    print()
    print("Customers table information:")
    print(f"Rows: {total_rows}")
    print(f"First event: {first_event}")
    print(f"Last event: {last_event}")
    print(f"Unique users: {unique_users}")
    print(f"Unique products: {unique_products}")


def main():
    total_rows, first_event, last_event, unique_users, unique_products = connect_and_load()
    print_all(
        total_rows,
        first_event,
        last_event,
        unique_users,
        unique_products
    )


if __name__ == "__main__":
    main()