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
    last_date = df["event_time"].max()

    rfm = df.groupby("user_id").agg(
        recency=("event_time", lambda x: (last_date - x.max()).days),
        frequency=("user_id", "count"),
        monetary=("price", "sum")
    )

    return rfm

def get_group(rfm):
    """
    Create 5 customer groups using KMeans.
    Assign commercial labels based on cluster characteristics.
    """
    scaler = StandardScaler()
    features = ["recency", "frequency", "monetary"]
    rfm_scaled = scaler.fit_transform(rfm[features])

    kmeans = KMeans(
        n_clusters=5,
        random_state=22,
        n_init=10
    )

    rfm["cluster"] = kmeans.fit_predict(rfm_scaled)
    stats = rfm.groupby("cluster")[features].mean()
    loyalty = stats.sort_values("monetary").index.tolist()
    inactive = stats["recency"].idxmax()
    other = [c for c in loyalty if c != inactive]
    other = sorted(other, key=lambda c: stats.loc[c, "monetary"])

    labels = {}
    labels[loyalty[-1]] = "Platinum"
    labels[loyalty[-2]] = "Gold"
    labels[loyalty[-3]] = "Silver"
    labels[inactive] = "Inactive"

    remaining = [c for c in stats.index if c not in labels]
    if remaining:
        labels[remaining[0]] = "New"

    rfm["customer_type"] = rfm["cluster"].map(labels)

    return rfm

def plot_groups(rfm):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    rfm["customer_type"].value_counts().plot(
        kind="bar", ax=axes[0]
    )
    axes[0].set_title("Customers per group")
    axes[0].set_xlabel("Customer type")
    axes[0].set_ylabel("Number of customers")

    for name, group in rfm.groupby("customer_type"):
        axes[1].scatter(
            group["frequency"],
            group["monetary"],
            label=name,
            alpha=0.6
        )
    axes[1].set_title("Frequency vs Monetary")
    axes[1].set_xlabel("Frequency")
    axes[1].set_ylabel("Monetary")
    axes[1].legend()

    for name, group in rfm.groupby("customer_type"):
        axes[2].scatter(
            group["recency"],
            group["monetary"],
            label=name,
            alpha=0.6
        )
    axes[2].set_title("Recency vs Monetary")
    axes[2].set_xlabel("Recency (days)")
    axes[2].set_ylabel("Monetary")
    axes[2].legend()

    plt.tight_layout()
    plt.show()
    
def main():
    df = readdb()
    rfm = find_rfm(df)
    rfm = get_group(rfm)
    plot_groups(rfm)

    print(rfm.head())
    
if __name__ == "__main__":
    main()