import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

def dbconnect():
	return psycopg2.connect(
    host="localhost",
    port=5432,
    user="csalamit",
    password="mysecretpassword",
    dbname="piscineds"
)

def readdb():
    connection = dbconnect()

    df = pd.read_sql("""
        SELECT *
        FROM customers
        WHERE event_type = 'purchase'
        ORDER BY event_time;
    """, connection)

    connection.close()
    return df

def main():
    df = readdb()

    print("Connected to PostgreSQL!")
    print("TOTAL PURCHASES =", len(df))
    print("MIN DATE =", df["event_time"].min())
    print("MAX DATE =", df["event_time"].max())



if __name__ == "__main__":
    main()
