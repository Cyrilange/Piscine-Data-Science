import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2
from dotenv import load_dotenv

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
    connection = dbconnect()

    df = pd.read_sql("""
        SELECT *
        FROM customers
        WHERE event_type = 'purchase'
        ORDER BY event_time;
    """, connection)

    connection.close()

    return df

def find_frequency(df):
    """
    Count purchases for each customer and group them by frequency range.
    Returns the number of customers in each range.
    """
    frequency = df.groupby("user_id").size()

    bins = pd.cut(
        frequency,
        bins=[0, 10, 20, 30, float("inf")],
        labels=["0", "10","20", "30"],
        right=False
    )

    return bins.value_counts().sort_index()

def graph_frequency(df):
    frequency = find_frequency(df)
    print(frequency)

    plt.bar(
        [5, 15, 25, 35],
        frequency.values,
        width=9,
        color="skyblue"
    )

    plt.xticks([0, 10, 20, 30])
    plt.xlim(-5, 45)
    plt.title("Number of customers by purchase frequency")
    plt.xlabel("Frequency")
    plt.ylabel("Customers")
    plt.show()

def find_monetary(df):
    """
    Calculate the total amount spent by each customer and group
    customers by total spending range.
    Returns the number of customers in each range.
    
    """
    monetary = df.groupby("user_id")["price"].sum()

    bins = pd.cut(
        monetary,
        bins=[0, 50, 100, 150, 200, float("inf")],
        labels=["0", "50", "100", "150", "200"],
        right=False
    )

    return bins.value_counts().sort_index()


def graph_monetary(df):
    monetary = find_monetary(df)
    print(monetary)

    plt.bar(
        [25, 75, 125, 175, 225],
        monetary.values,
        width=40,
        color="skyblue"
    )

    plt.xticks([0, 50, 100, 150, 200])
    plt.xlim(0, 250)

    plt.title("Number of customers by total spend")
    plt.xlabel("Monetary values in A")
    plt.ylabel("Customers")
    plt.show()
    

def main():
    df = readdb()
    graph_frequency(df)
    graph_monetary(df)

    

    
if __name__ == main():
    main()