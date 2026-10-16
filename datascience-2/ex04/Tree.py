
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import sys


def create_validation(df):
    training = df.sample(frac=0.8, random_state=42)
    remaining_indexes = df.index.difference(training.index)
    validation = df.loc[remaining_indexes]

    training.to_csv("Training_knight.csv", index=False)
    validation.to_csv("Validation_knight.csv", index=False)

    return training, validation


def main():
    if len(sys.argv) != 3:
        print("Usage: .venv/bin/python Tree.py ../Train_knight.csv ../Test_knight.csv")
        return

    train_file = sys.argv[1]
    test_file = sys.argv[2]

    try:
        df = pd.read_csv(train_file)
        testing = pd.read_csv(test_file)
    except FileNotFoundError as error:
        print(error)
        return

    training, validation = create_validation(df)

    X_train = training.drop(columns=["knight"])
    y_train = training["knight"]

    X_validation = validation.drop(columns=["knight"])
    y_validation = validation["knight"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_validation)
    score = f1_score(y_validation, y_pred, pos_label="Jedi")
    print("F1-score:", score)


    fig, ax = plt.subplots(figsize=(28, 14))

    plot_tree(
        model.estimators_[0],
        feature_names=X_train.columns,
        class_names=[str(c) for c in model.classes_],
        filled=True,
        rounded=True,
        proportion=True,
        impurity=False,
        max_depth=7,
        precision=2,
        fontsize=9,
        ax=ax
    )

    ax.set_title(
        "Random Forest — Decision Tree",
        fontsize=20,
        fontweight="bold",
        pad=20
    )

    fig.tight_layout()
    fig.savefig(
        "Tree.png",
        dpi=200,
        bbox_inches="tight",
        facecolor="white"
    )
    plt.show()
    plt.close(fig)


    model.fit(df.drop(columns=["knight"]), df["knight"])

    predictions = model.predict(testing)

    with open("Tree.txt", "w") as file:
        for prediction in predictions:
            file.write(str(prediction) + "\n")


if __name__ == "__main__":
    main()
