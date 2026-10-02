import psycopg2


def connect_db():
    print("[1/5] Connecting to PostgreSQL...")

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )

    print("[OK] Connected to database 'piscineds'.")
    return connection


def check_tables(connection):
    print()
    print("[2/5] Checking required tables...")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'customers'
        )
    """)
    customers_exists = cursor.fetchone()[0]

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'items'
        )
    """)
    items_exists = cursor.fetchone()[0]

    if not customers_exists:
        cursor.close()
        raise RuntimeError("Table 'customers' does not exist.")

    if not items_exists:
        cursor.close()
        raise RuntimeError("Table 'items' does not exist.")

    print("[OK] Table 'customers' found.")
    print("[OK] Table 'items' found.")

    cursor.close()


def get_counts(connection):
    print()
    print("[3/5] Checking data before fusion...")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM items")
    items_count = cursor.fetchone()[0]

    print(f"[INFO] Customers rows: {customers_count}")
    print(f"[INFO] Items rows: {items_count}")

    cursor.close()

    return customers_count, items_count


def fusion_tables(connection):
    print()
    print("[4/5] Running fusion...")

    cursor = connection.cursor()

    with open("fusion.sql", "r", encoding="utf-8") as sql_file:
        sql = sql_file.read()

    cursor.execute(sql)

    print("[OK] Fusion SQL executed.")

    connection.commit()

    print("[OK] Changes committed to PostgreSQL.")

    cursor.close()


def check_result(connection, customers_count_before):
    print()
    print("[5/5] Checking fusion result...")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers_count_after = cursor.fetchone()[0]

    print(f"[INFO] Customers rows before: {customers_count_before}")
    print(f"[INFO] Customers rows after:  {customers_count_after}")

    if customers_count_before == customers_count_after:
        print("[OK] No customer rows were lost.")
    else:
        print("[WARNING] The number of customer rows changed.")


    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'customers'
          AND column_name IN (
              'category_id',
              'category_code',
              'brand'
          )
        ORDER BY column_name
    """)

    columns = [row[0] for row in cursor.fetchall()]

    print()
    print("[INFO] New columns:")
    for column in columns:
        print(f"  - {column}")

    # 3. Vérifier les correspondances avec items
    cursor.execute("""
        SELECT COUNT(*)
        FROM customers c
        INNER JOIN items i
            ON c.product_id = i.product_id
    """)

    matched_rows = cursor.fetchone()[0]

   
    cursor.execute("""
        SELECT COUNT(*)
        FROM customers c
        LEFT JOIN items i
            ON c.product_id = i.product_id
        WHERE i.product_id IS NULL
    """)

    unmatched_rows = cursor.fetchone()[0]

    print()
    print(f"[INFO] Customers matched with items:   {matched_rows}")
    print(f"[INFO] Customers without matching item: {unmatched_rows}")

    if unmatched_rows == 0:
        print("[OK] All customers have a matching item.")
    else:
        print("[INFO] Some customers have no matching item.")

   
    cursor.execute("""
        SELECT
            product_id,
            category_id,
            category_code,
            brand
        FROM customers
        WHERE category_id IS NOT NULL
        LIMIT 5
    """)

    sample_rows = cursor.fetchall()

    print()
    print("[INFO] Sample of merged data:")
    print("----------------------------------------")

    for row in sample_rows:
        product_id, category_id, category_code, brand = row

        print(f"Product ID:    {product_id}")
        print(f"Category ID:   {category_id}")
        print(f"Category code: {category_code}")
        print(f"Brand:         {brand}")
        print("----------------------------------------")

    cursor.close()


def main():
    print("========================================")
    print("        EX03 : FUSION")
    print("========================================")

    connection = None

    try:
        connection = connect_db()

        check_tables(connection)

        customers_count, items_count = get_counts(connection)

        fusion_tables(connection)

        check_result(connection, customers_count)

        print()
        print("========================================")
        print("        FUSION COMPLETED")
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
    


