import psycopg2


def connect_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
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