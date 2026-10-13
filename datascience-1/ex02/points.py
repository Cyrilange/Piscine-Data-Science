import pandas as pd
import matplotlib.pyplot as plt


def open_file_test():
    return pd.read_csv("../Test_knight.csv")


def open_file_train():
    return pd.read_csv("../Train_knight.csv")


def fn_read_csv():
    train = open_file_train()
    test = open_file_test()
    # print(train.info())
    # print(test.info())

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ax = axes[0,0]

  
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

    axes[0, 0].set_title("Train - Separate")
    axes[0, 0].set_xlabel("Hability")
    axes[0, 0].set_ylabel("Sensitivity")
    axes[0, 0].legend()

    for knight in train["knight"].unique():
        group = train[train["knight"] == knight]
        axes[0, 1].scatter(
            group["Mass"],
            group["Push"],
            label=knight,
            s=20
        )

    axes[0, 1].set_title("Train - Mixed")
    axes[0, 1].set_xlabel("Mass")
    axes[0, 1].set_ylabel("Push")
    axes[0, 1].legend()

    axes[1, 0].scatter(test["Hability"], test["Sensitivity"], s=20)
    axes[1, 0].set_title("Test - Separate features")
    axes[1, 0].set_xlabel("Hability")
    axes[1, 0].set_ylabel("Sensitivity")

    axes[1, 1].scatter(test["Mass"], test["Push"], s=20)
    axes[1, 1].set_title("Test - Mixed features")
    axes[1, 1].set_xlabel("Mass")
    axes[1, 1].set_ylabel("Push")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fn_read_csv()