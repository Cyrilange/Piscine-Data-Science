import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="csalamit",
    password="mysecretpassword",
    dbname="piscineds"
)

cursor = connection.cursor()

cursor.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'data_2022_oct'
    )
""")

table_exists = cursor.fetchone()[0]

if table_exists:
    print("Table data_2022_oct already exists")
else:
    with open("table.sql", "r") as sql_file:
        cursor.execute(sql_file.read())

    with open("customer/data_2022_oct.csv", "r") as csv_file:
        cursor.copy_expert(
            "COPY data_2022_oct FROM STDIN WITH (FORMAT csv, HEADER true, NULL '')",
            csv_file
        )

    connection.commit()
    print("Table created and data imported")

cursor.close()
connection.close()