import matplotlib.pyplot as plt
import pandas as pd

def read_train():
    dfTrain = pd.read_csv("../Train_knight.csv")
    return dfTrain

def read_test():
    dfTest = pd.read_csv("../Test_knight.csv")
    return dfTest



def normalization(df, name, minimum=None, maximum=None):
    numeric_cols = df.select_dtypes(include="number").columns
    df_normalized = df.copy()

    if minimum is None:
        minimum = df[numeric_cols].min()
        maximum = df[numeric_cols].max()

    denominator = (maximum - minimum).replace(0, 1)

    df_normalized[numeric_cols] = (
        (df[numeric_cols] - minimum) / denominator
    )

    print(name)
    print(df_normalized)

    return df_normalized, minimum, maximum


def graph_df(train, test):
    fig, ax = plt.subplots(figsize=(8, 6))

    for knight in train["knight"].unique():
        group = train[train["knight"] == knight]

        ax.scatter(
            group["Mass"],
            group["Push"],
            label=knight,
            s=20
        )

    ax.set_xlabel("Mass")
    ax.set_ylabel("Push")
    ax.set_title("Mass vs Push (normalized)")
    ax.legend()
    plt.tight_layout()
    plt.show()

    

def main():
    train = read_train()
    test = read_test()


    train, minimum, maximum = normalization(
        train, "Train_knight.csv"
    )

    print(f"min : {train[['Mass', 'Push']].min()}")
    print(f"mean : {train[['Mass', 'Push']].mean()}")
    print(f"median : {train[['Mass', 'Push']].median()}")
    print(f"max : {train[['Mass', 'Push']].max()}")

    test, _, _ = normalization(
        test, "Test_knight.csv", minimum, maximum
    )

    graph_df(train, test)

if __name__ == "__main__":
    main()
