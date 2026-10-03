import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )


def create_and_load_items():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'items'
        )
    """)

    table_exists = cursor.fetchone()[0]

    if table_exists:
        cursor.execute("SELECT COUNT(*) FROM item")
        row_count = cursor.fetchone()[0]

        print("Table items already exists")
        print(f"Rows: {row_count}")

    else:
        with open("items_table.sql", "r") as sql_file:
            cursor.execute(sql_file.read())

        with open("subject/item/item.csv", "r") as csv_file:
            cursor.copy_expert(
                "COPY items FROM STDIN WITH (FORMAT csv, HEADER true, NULL '')",
                csv_file
            )

        cursor.execute("SELECT COUNT(*) FROM items")
        row_count = cursor.fetchone()[0]

        connection.commit()

        print("Table items created and data imported")
        print(f"Rows: {row_count}")

    cursor.close()
    connection.close()


def main():
    print("=== EX04 : ITEMS TABLE ===")
    print()

    create_and_load_items()

    print()
    print("Process finished.")


if __name__ == "__main__":
    main()


# psql -U csalamit -d piscineds -h localhost -W -c "\d items"

# psql -U csalamit -d piscineds -h localhost -W -c "SELECT COUNT(*) FROM items;"