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
		SELECT event_type, COUNT(*) AS count
		FROM customers
		GROUP BY event_type
		ORDER BY count DESC;
	""", connection)
	return df

def main():
    connection = dbconnect()
    df = readdb()

    print("Connected to PostgreSQL!")
    print("TOTAL =", df["count"].sum())
    print("PURCHASE =", df.loc[df["event_type"] == "purchase", "count"].iloc[0])
    plt.pie(df["count"], labels=df["event_type"], autopct="%1.1f%%")
    plt.savefig("pie.png")
    plt.show()

    connection.close()


if __name__ == "__main__":
    main()
