import psycopg2
import csv

def analyze_csv():
    with open("customer/data_2022_oct.csv","r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    print("=== CSV INFORMATION ===")
    print(f"Number of rows: {len(rows)}")
    print(f"Number of columns: {len(reader.fieldnames)}")
    print()

    for column in reader.fieldnames:
        values = [ row[column] for row in rows if row[column] != "" ]

        print(f"Column: {column}")
        print(f"  Non-null values: {len(values)}")

        if not values:
            print("  Empty column")
            print()
            continue

        if all(value.isdigit() for value in values):
            numbers = [int(value) for value in values]

            print("  Detected type: INTEGER")
            print(f"  Min: {min(numbers)}")
            print(f"  Max: {max(numbers)}")

        else:
            print(f"  First value: {values[0]}")

        print()

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )


def create_and_load():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name = 'data_2022_oct'
                )
            """)

            table_exists = cursor.fetchone()[0]

            if table_exists:
                print("Table data_2022_oct already exists")
                return False

            with open("table.sql", "r", encoding="utf-8") as sql_file:
                cursor.execute(sql_file.read())

            with open(
                "customer/data_2022_oct.csv",
                "r",
                encoding="utf-8"
            ) as csv_file:
                cursor.copy_expert(
                    """
                    COPY data_2022_oct
                    FROM STDIN
                    WITH (
                        FORMAT csv,
                        HEADER true,
                        NULL ''
                    )
                    """,
                    csv_file
                )

            connection.commit()
            return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def main():
    print("=== EX02 : FIRST TABLE ===")
    print()

    analyze_csv()

    print()
    print("Creating PostgreSQL table...")

    created = create_and_load()

    print()

    if created:
        print("Table 'data_2022_oct' created.")
        print("CSV data imported.")
    else:
        print("Table 'data_2022_oct' already exists.")
        print("Nothing to import.")

    print()
    print("=== Done ===")


if __name__ == "__main__":
    main()