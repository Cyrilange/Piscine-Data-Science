import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def dbconnect():
    """
    Connect to the PostgreSQL database.
    Returns the database connection.
    """
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
)

def readdb():
    """
    Read purchase data from the customers table.
    Returns the data as a Pandas DataFrame.
    """
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
    # print("TOTAL =", df["count"].sum())
    # print("PURCHASE =", df.loc[df["event_type"] == "purchase", "count"].iloc[0])
    plt.title("Pie", fontsize=16, fontweight="bold")
    plt.pie(df["count"], labels=df["event_type"], autopct="%1.1f%%", startangle=50)
    # plt.savefig("pie.png")
    plt.show()

    connection.close()


if __name__ == "__main__":
    main()
