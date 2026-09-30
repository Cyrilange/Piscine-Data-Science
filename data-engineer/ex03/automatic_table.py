import os
import psycopg2
from psycopg2 import sql


def main():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )

    cursor = connection.cursor()

    customer_dir = "customer"

    if not os.path.isdir(customer_dir):
        customer_dir = "subject/customer"

    if not os.path.isdir(customer_dir):
        raise FileNotFoundError(
            "Neither 'customer' nor 'subject/customer' exists."
        )

    csv_files = sorted(
        filename
        for filename in os.listdir(customer_dir)
        if filename.endswith(".csv")
    )

    print("=== EX03 : AUTOMATIC TABLE CREATION ===")
    print(f"Customer directory: {customer_dir}")
    print(f"CSV files found: {len(csv_files)}")
    print()

    created = 0
    skipped = 0
    total_rows = 0

    try:
        for filename in csv_files:
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
                cursor.execute(
                    sql.SQL("SELECT COUNT(*) FROM {}").format(
                        sql.Identifier(table_name)
                    )
                )

                row_count = cursor.fetchone()[0]

                print(f"{table_name}: already exists")
                print(f"  Rows: {row_count}")

                skipped += 1
                total_rows += row_count
                continue

            cursor.execute(
                sql.SQL("""
                    CREATE TABLE {} (
                        event_time TIMESTAMP WITH TIME ZONE,
                        event_type TEXT,
                        product_id BIGINT,
                        price NUMERIC,
                        user_id BIGINT,
                        user_session UUID
                    )
                """).format(
                    sql.Identifier(table_name)
                )
            )

            csv_path = os.path.join(customer_dir, filename)

            with open(csv_path, "r", encoding="utf-8") as csv_file:
                cursor.copy_expert(
                    sql.SQL("""
                        COPY {}
                        FROM STDIN
                        WITH (
                            FORMAT csv,
                            HEADER true,
                            NULL ''
                        )
                    """).format(
                        sql.Identifier(table_name)
                    ).as_string(connection),
                    csv_file
                )

            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM {}").format(
                    sql.Identifier(table_name)
                )
            )

            row_count = cursor.fetchone()[0]

            print(f"{table_name}: created and imported")
            print(f"  Rows: {row_count}")

            created += 1
            total_rows += row_count

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

    print()
    print("=== SUMMARY ===")
    print(f"Tables created: {created}")
    print(f"Tables already existing: {skipped}")
    print(f"Total rows: {total_rows}")


if __name__ == "__main__":
    main()