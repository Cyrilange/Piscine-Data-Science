import csv
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    print("Connecting to PostgreSQL...")

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
    )

    print("[OK] Connected to database 'piscineds'.")
    return connection


def load_february(connection):
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

    with open("../data_2023_feb.csv", "r") as file:
        next(file)
        cursor.copy_expert(
            """
            COPY data_2023_feb
            FROM STDIN
            WITH CSV
            """,
            file
        )

    connection.commit()
    cursor.close()

def create_customers(connection):
    print()
    print("Creating customers table...")

    cursor = connection.cursor()

    with open("customers_table.sql", "r", encoding="utf-8") as sql_file:
        cursor.execute(sql_file.read())

    connection.commit()

    print("[OK] Table 'customers' created.")

    cursor.close()



def main():
    print("========================================")
    print("        EX01 : CUSTOMERS TABLE")
    print("========================================")

    connection = None

    try:
        connection = connect_db()

        load_february(connection)
        create_customers(connection)


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
