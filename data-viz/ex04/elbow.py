import pandas as pd
import os
import matplotlib.pyplot as plt
import psycopg2
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
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


def find_rfm(df):
    """
    Calculate Recency, Frequency and Monetary for each customer.
    Returns the RFM dataframe.
    """
    last_date = df["event_time"].max()

    rfm = df.groupby("user_id").agg(
        recency=("event_time", lambda x: (last_date - x.max()).days),
        frequency=("user_id", "count"),
        monetary=("price", "sum")
    )

    return rfm


def graph_rfm(rfm):
    """
    Calculate the inertia for different numbers of clusters
    and display the Elbow Method graph.
    """
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)

    inertias = []

    for k in range(1, 11):
        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        kmeans.fit(rfm_scaled)

        inertias.append(kmeans.inertia_)

    plt.plot(range(1, 11), inertias, marker="o")
    plt.xticks(range(1, 11))
    plt.axvline(x=4, color="red", linestyle="--")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.scatter(4, inertias[3], color="red", s=100)
    plt.show()


def main():
    df = readdb()

    rfm = find_rfm(df)
    rfm.index = rfm.index.astype(int)
    rfm = rfm.sort_index()

    print(rfm.iloc[:10])

    graph_rfm(rfm)


if __name__ == "__main__":
    main()