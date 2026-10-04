import csv
import psycopg2


def connect_db():
    print("[1/6] Connecting to PostgreSQL...")

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )

    print("[OK] Connected to database 'piscineds'.")
    return connection


def load_february(connection):
    print()
    print("[2/6] Loading data_2023_feb.csv...")

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS data_2023_feb")

    cursor.execute("""
        CREATE TABLE data_2023_feb (
            event_time TIMESTAMPTZ,
            event_type TEXT,
            product_id BIGINT,
            price NUMERIC,
            user_id INT,
            user_session UUID
        )
    """)

    with open("../data_2023_feb.csv", "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)

        rows = []

        for row in reader:
            rows.append((
                row[0] if row[0] else None,
                row[1] if row[1] else None,
                int(row[2]) if row[2] else None,
                float(row[3]) if row[3] else None,
                int(row[4]) if row[4] else None,
                row[5] if row[5] else None
            ))

            if len(rows) >= 10000:
                cursor.executemany("""
                    INSERT INTO data_2023_feb
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, rows)
                rows = []

        if rows:
            cursor.executemany("""
                INSERT INTO data_2023_feb
                VALUES (%s, %s, %s, %s, %s, %s)
            """, rows)

    connection.commit()

    print("[OK] data_2023_feb loaded.")

    cursor.close()


def create_customers(connection):
    print()
    print("[3/6] Creating customers table...")

    cursor = connection.cursor()

    with open("customers_table.sql", "r", encoding="utf-8") as sql_file:
        cursor.execute(sql_file.read())

    connection.commit()

    print("[OK] Table 'customers' created.")

    cursor.close()


def get_statistics(connection):
    print()
    print("[4/6] Calculating customers statistics...")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
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

    return total_rows, first_event, last_event, unique_users, unique_products


def print_statistics(
    total_rows,
    first_event,
    last_event,
    unique_users,
    unique_products
):
    print()
    print("[5/6] Customers table information:")
    print("----------------------------------------")
    print(f"Rows:            {total_rows}")
    print(f"First event:     {first_event}")
    print(f"Last event:      {last_event}")
    print(f"Unique users:    {unique_users}")
    print(f"Unique products: {unique_products}")
    print("----------------------------------------")


def main():
    print("========================================")
    print("        EX01 : CUSTOMERS TABLE")
    print("========================================")

    connection = None

    try:
        connection = connect_db()

        load_february(connection)
        create_customers(connection)

        statistics = get_statistics(connection)

        print_statistics(*statistics)

        print()
        print("========================================")
        print("        EX01 COMPLETED")
        print("========================================")

    except Exception as error:
        print()
        print("========================================")
        print("        ERROR")
        print("========================================")
        print(f"[ERROR] {error}")

        if connection is not None:
            connection.rollback()
            print("[INFO] Transaction rolled back.")

    finally:
        if connection is not None:
            connection.close()
            print("[INFO] Database connection closed.")


if __name__ == "__main__":
    main()
