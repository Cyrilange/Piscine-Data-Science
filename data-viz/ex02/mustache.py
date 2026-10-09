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
    pd.set_option("display.float_format", "{:.2f}".format)
    print(df["price"].describe())
    plt.figure(figsize=(9, 3))

    plt.boxplot(
        df["price"],
        orientation="horizontal",
        showfliers=False,
        patch_artist=True,
        boxprops={"facecolor": "#A0C4E8", "edgecolor": "#4C78A8"},
        medianprops={"color": "#E45756", "linewidth": 1.5},
        whiskerprops={"color": "#4C78A8"},
        capprops={"color": "#4C78A8"}
    )

    plt.xlabel("Price")
    plt.title("Price of purchased items (A)")
    plt.grid(axis="x", alpha=0.3)
    plt.show()
     
def prepare_data_per_user(df):
    pd.set_option("display.float_format", "{:.2f}".format)
    average_price_per_user = df.groupby("user_id")["price"].mean()
    print(average_price_per_user.describe())
   
    plt.boxplot(
    average_price_per_user,
    orientation="horizontal",
    showfliers=False,
    patch_artist=True,
    boxprops={"facecolor": "#A0C4E8", "edgecolor": "#4C78A8"},
    medianprops={"color": "#E45756", "linewidth": 1.5},
    whiskerprops={"color": "#4C78A8"},
    capprops={"color": "#4C78A8"}
)
    plt.xlabel("Price")
    plt.title("Average basket(total spend per user) (A)")
    plt.grid(axis="x", alpha=0.3)
    plt.show()

def main():
    df = readdb()
    prepare_data(df)
    prepare_data_per_user(df)


if __name__ == "__main__":
    main()