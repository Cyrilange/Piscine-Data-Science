import csv
import os
from datetime import datetime

import psycopg2


TABLE_NAME = "data_2022_oct"


def find_customer_dir():
    """Find the customer directory."""

    customer_dir = "customer"

    if not os.path.isdir(customer_dir):
        customer_dir = "subject/customer"

    if not os.path.isdir(customer_dir):
        raise FileNotFoundError(
            "Neither 'customer' nor 'subject/customer' exists."
        )

    return customer_dir


def get_connection():
    """Connect to PostgreSQL."""

    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="csalamit",
        password="mysecretpassword",
        dbname="piscineds"
    )


def find_csv_file(customer_dir):
    """Find data_2022_oct.csv."""

    csv_file = os.path.join(
        customer_dir,
        "data_2022_oct.csv"
    )

    if not os.path.isfile(csv_file):
        raise FileNotFoundError(
            f"CSV file not found: {csv_file}"
        )

    return csv_file


def read_csv(csv_file):
    """Read the CSV file."""

    with open(
        csv_file,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header.")

        rows = list(reader)

    return reader.fieldnames, rows


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_boolean(value):
    return value.lower() in (
        "true",
        "false",
        "yes",
        "no"
    )


def is_timestamp(value):
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d"
    ]

    for date_format in formats:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            pass

    return False


def detect_column_type(values, first_column=False):
    """Detect a PostgreSQL type."""

    values = [
        value.strip()
        for value in values
        if value is not None and value.strip() != ""
    ]

    if not values:
        return "TEXT"

    # First column must be a datetime.
    if first_column and all(
        is_timestamp(value)
        for value in values
    ):
        return "TIMESTAMP"

    if all(is_boolean(value) for value in values):
        return "BOOLEAN"

    if all(is_integer(value) for value in values):
        return "INTEGER"

    if all(is_numeric(value) for value in values):
        return "NUMERIC"

    if all(is_timestamp(value) for value in values):
        return "TIMESTAMP"

    return "TEXT"


def analyze_csv(headers, rows):
    """Analyze CSV columns."""

    print("=== CSV INFORMATION ===")
    print(f"Number of rows: {len(rows)}")
    print(f"Number of columns: {len(headers)}")
    print()

    column_types = {}

    for index, column in enumerate(headers):

        values = [
            row[column]
            for row in rows
            if row[column] is not None
            and row[column].strip() != ""
        ]

        column_type = detect_column_type(
            values,
            first_column=(index == 0)
        )

        column_types[column] = column_type

        print(f"Column: {column}")
        print(f"  Non-null values: {len(values)}")
        print(f"  Detected type: {column_type}")

        if column_type == "INTEGER":
            numbers = [int(value) for value in values]
            print(f"  Min: {min(numbers)}")
            print(f"  Max: {max(numbers)}")

        elif column_type == "NUMERIC":
            numbers = [float(value) for value in values]
            print(f"  Min: {min(numbers)}")
            print(f"  Max: {max(numbers)}")

        elif values:
            print(f"  First value: {values[0]}")

        print()

    return column_types


def quote_identifier(identifier):
    """Safely quote a PostgreSQL identifier."""

    return '"' + identifier.replace('"', '""') + '"'


def table_exists(connection):
    """Check if the table already exists."""

    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (TABLE_NAME,)
        )

        return cursor.fetchone()[0]


def create_table(connection, headers, column_types):
    """Create PostgreSQL table."""

    columns = []

    for column in headers:

        column_name = quote_identifier(column)
        column_type = column_types[column]

        columns.append(
            f"{column_name} {column_type}"
        )

    query = f"""
        CREATE TABLE {quote_identifier(TABLE_NAME)} (
            {", ".join(columns)}
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

    connection.commit()


def load_csv(connection, csv_file):
    """Import CSV into PostgreSQL."""

    with open(
        csv_file,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        with connection.cursor() as cursor:

            cursor.copy_expert(
                f"""
                COPY {quote_identifier(TABLE_NAME)}
                FROM STDIN
                WITH (
                    FORMAT CSV,
                    HEADER TRUE,
                    NULL ''
                )
                """,
                file
            )

    connection.commit()


def main():

    print("=== EX02 : FIRST TABLE ===")
    print()

    customer_dir = find_customer_dir()

    print(f"Customer directory: {customer_dir}")

    csv_file = find_csv_file(customer_dir)

    print(f"CSV file: {csv_file}")
    print()

    headers, rows = read_csv(csv_file)
    column_types = analyze_csv(
        headers,
        rows
    )

    # Connect to PostgreSQL.
    print("Connecting to PostgreSQL...")

    connection = get_connection()

    try:

        if table_exists(connection):

            print()
            print(
                f"Table '{TABLE_NAME}' already exists."
            )
            print("Nothing to import.")

            return

        print()
        print(
            f"Creating table '{TABLE_NAME}'..."
        )

        create_table(
            connection,
            headers,
            column_types
        )

        print("Table created.")

        print()
        print("Importing CSV data...")

        load_csv(
            connection,
            csv_file
        )

        print("CSV data imported.")

        print()
        print("=== Done ===")

    except Exception as error:

        connection.rollback()

        print()
        print("ERROR:")
        print(error)

        raise

    finally:

        connection.close()


if __name__ == "__main__":
    main()