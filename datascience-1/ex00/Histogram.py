import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def open_file_test():
    return pd.read_csv("../Test_knight.csv")

def open_file_train():
    return pd.read_csv("../Train_knight.csv")

def read_csv_test():
    df = open_file_test()
    columns = df.select_dtypes(include="number").columns

    cols = 5
    rows = int(np.ceil(len(columns) / cols))

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(14, 2.4 * rows),
        layout="constrained"
    )

    axes = np.atleast_1d(axes).ravel()

    for i, col in enumerate(columns):
        ax = axes[i]
        ax.hist(df[col].dropna(), bins=20,color="green", edgecolor="white", alpha=0.9)
        ax.set_title(col, fontsize=8)
        ax.tick_params(labelsize=6)

    for i in range(len(columns), len(axes)):
        axes[i].set_visible(False)

    plt.show()
    

def read_csv_train():
    df = open_file_train()

    target = "knight"
    columns = [
        col for col in df.select_dtypes(include="number").columns
        if col != target
    ]

    cols = 5
    rows = int(np.ceil(len(columns) / cols))

    fig, axes = plt.subplots(
        rows, cols,
        figsize=(14, 2.4 * rows),
        layout="constrained"
    )

    axes = np.atleast_1d(axes).ravel()

    colors = {
        "Jedi": "green",
        "Sith": "red"
    }

    for i, col in enumerate(columns):
        ax = axes[i]

        for knight, color in colors.items():
            data = df.loc[df[target] == knight, col].dropna()

            ax.hist(
                data,
                bins=20,
                color=color,
                alpha=0.5,
                edgecolor="white",
                label=knight
            )

        ax.set_title(col, fontsize=8)
        ax.tick_params(labelsize=6)

    for i in range(len(columns), len(axes)):
        axes[i].set_visible(False)

    fig.legend(
        ["Jedi", "Sith"],
        loc="upper right"
    )

    plt.show()
    
def main():
    read_csv_test()
    read_csv_train()

if __name__ == "__main__":
	main()
