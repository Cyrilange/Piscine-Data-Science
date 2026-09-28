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
        WHERE table_name = 'items'
    )
""")

table_exists = cursor.fetchone()[0]

if table_exists:
    print("Table items already exists")
else:
    with open("items_table.sql", "r") as sql_file:
        cursor.execute(sql_file.read())

    with open("subject/items/item.csv", "r") as csv_file:
        cursor.copy_expert(
            "COPY items FROM STDIN WITH (FORMAT csv, HEADER true, NULL '')",
            csv_file
        )

    connection.commit()
    print("Table created and data imported")

cursor.close()
connection.close()

#  psql -U csalamit -d piscineds -h localhost -W -c "\d items"

# psql -U csalamit -d piscineds -h localhost -W -c "SELECT COUNT(*) FROM items;"