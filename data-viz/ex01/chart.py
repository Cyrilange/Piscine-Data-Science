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


def prepare_data(df):
    df["event_time"] = pd.to_datetime(df["event_time"])

    return df


def create_monthly_customers_chart(df):
    monthly_customers = (
        df.set_index("event_time")
        .resample("MS")["user_id"]
        .nunique()
    )

    plt.figure(figsize=(10, 5))
    monthly_customers.plot(kind="line", marker="o")

    plt.xlabel("Month")
    plt.ylabel("Number of customers")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("chart_number_customers.png")
    plt.show()


def create_monthly_sales_chart(df):
    monthly_sales = (
        df.set_index("event_time")["price"]
        .resample("MS")
        .sum()
        / 1_000_000
    )

    plt.figure(figsize=(10, 5))
    monthly_sales.plot(kind="line", marker="o")

    plt.xlabel("Month")
    plt.ylabel("Total sales (millions of A)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("chart_total_sales.png")
    plt.show()


def create_monthly_average_spend_chart(df):
    monthly_sales = (
        df.set_index("event_time")["price"]
        .resample("MS")
        .sum()
    )

    monthly_customers = (
        df.set_index("event_time")["user_id"]
        .resample("MS")
        .nunique()
    )

    average_spend = monthly_sales / monthly_customers

    plt.figure(figsize=(10, 5))
    average_spend.plot(kind="line", marker="o")

    plt.xlabel("Month")
    plt.ylabel("Average spend per customer (A)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("chart_average_spend.png")
    plt.show()

def main():
    df = readdb()

    print("Connected to PostgreSQL!")
    print("TOTAL PURCHASES =", len(df))
    print("MIN DATE =", df["event_time"].min())
    print("MAX DATE =", df["event_time"].max())

    df = prepare_data(df)

    create_monthly_customers_chart(df)
    create_monthly_sales_chart(df)
    create_monthly_average_spend_chart(df)


if __name__ == "__main__":
    main()