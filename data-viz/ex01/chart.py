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
    """
    Read purchase data from the customers table.
    Returns the data as a Pandas DataFrame.
    """
    connection = dbconnect()

    df = pd.read_sql("""
        SELECT *
        FROM customers
        WHERE event_type = 'purchase'
        ORDER BY event_time;
    """, connection)

    connection.close()

    return df


def prepare_data(df):
    df["event_time"] = pd.to_datetime(df["event_time"])

    return df


def create_daily_customers_chart(df):
    monthly_customers = (
        df.set_index("event_time")["user_id"]
        .resample("D")
        .nunique()
    )

    plt.figure(figsize=(10, 5))
    monthly_customers.plot(kind="line")

    plt.xlabel("Month")
    plt.ylabel("Number of customers")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def create_monthly_sales_chart(df):
    monthly_sales = (
        df.set_index("event_time")["price"]
        .resample("MS")
        .sum()
        / 1_000_000
    )

    monthly_sales.index = monthly_sales.index.strftime("%b")

    plt.figure(figsize=(8, 5))

    monthly_sales.plot(
        kind="bar",
        edgecolor="white"
    )

    plt.xlabel("Month")
    plt.ylabel("Total sales in million of A")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()


def create_daily_average_spend_chart(df):
    daily_average = (
        df.set_index("event_time")["price"]
        .resample("D")
        .mean()
    ) * 10

    plt.figure(figsize=(10, 5))

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    plt.fill_between(
        daily_average.index,
        daily_average.values,
        alpha=0.45
    )

    plt.plot(
        daily_average.index,
        daily_average.values,
        linewidth=0.8
    )

    plt.xlabel("Month")
    plt.ylabel("Average spend per customer (A)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    df = readdb()

    print("Connected to PostgreSQL!")
    print("MIN DATE =", df["event_time"].min())
    print("MAX DATE =", df["event_time"].max())

    df = prepare_data(df)

    create_daily_customers_chart(df)
    create_monthly_sales_chart(df)
    create_daily_average_spend_chart(df)


if __name__ == "__main__":
    main()