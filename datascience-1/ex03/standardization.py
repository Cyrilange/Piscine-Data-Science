import matplotlib.pyplot as plt
import pandas as pd

def read_train():
    dfTrain = pd.read_csv("../Train_knight.csv")
    return dfTrain

def read_test():
    dfTest = pd.read_csv("../Test_knight.csv")
    return dfTest

def standardization(df, name):
    numeric_cols = df.select_dtypes(include="number").columns

    mean = df[numeric_cols].mean()
    std = df[numeric_cols].std(ddof=0)

    df[numeric_cols] = (df[numeric_cols] - mean) / std.replace(0, 1)

    print(name)
    print(df)
    return df





def graph_df(train, test):
    fig, ax = plt.subplots(figsize=(8, 6))

    for knight in train["knight"].unique():
        group = train[train["knight"] == knight]

        ax.scatter(
            group["Hability"],
            group["Sensitivity"],
            label=knight,
            s=20
        )

    ax.scatter(
        test["Hability"],
        test["Sensitivity"],
        color=[
            plt.get_cmap("tab10")(
                list(train["knight"].unique()).index(k)
            )
            for k in train["knight"].unique()
        ][0],
        s=20,
        alpha=0.7
    )

    ax.set_title("Train and Test - Standardized")
    ax.set_xlabel("Hability")
    ax.set_ylabel("Sensitivity")
    ax.legend()
    plt.tight_layout()
    plt.show()

    
def main():
    train = read_train()
    test = read_test()

    train = standardization(train, "Train_knight.csv")
    test = standardization(test, "Test_knight.csv")
    
    graph_df(train, test)

if __name__ == "__main__":
    main()