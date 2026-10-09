import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
    )


def remove_duplicates(connection):
    cursor = connection.cursor()

    with open("remove_duplicates.sql", "r", encoding="utf-8") as sql_file:
        sql = sql_file.read()

    cursor.execute(sql)

    removed_rows = cursor.rowcount

    connection.commit()
    cursor.close()

    return removed_rows


def main():
    print("=== EX02 : REMOVE DUPLICATES ===")

    connection = connect_db()

    try:
        removed_rows = remove_duplicates(connection)

        print(f"Duplicates removed: {removed_rows}")

    except Exception as error:
        connection.rollback()
        print(f"Error: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()