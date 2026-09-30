import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="csalamit",
    password="mysecretpassword",
    dbname="piscineds"
)

cursor = connection.cursor()

# Remove duplicates
with open("remove_duplicates.sql", "r") as sql_file:
    cursor.execute(sql_file.read())

removed_rows = cursor.fetchall()

connection.commit()

print(f"Duplicates removed: {len(removed_rows)}")

for event_time, event_type, product_id in removed_rows:
    print(f"{event_time} | {event_type} | {product_id}")

cursor.close()
connection.close()