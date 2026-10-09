import pandas as pd

def correlation():
    df = pd.read_csv("../Train_knight.csv")

    df["knight"] = df["knight"].map({
        "Jedi": 1,
        "Sith": 0
    })

    corr = df.corr(numeric_only=True)["knight"]
    corr = corr.reindex(
        corr.abs().sort_values(ascending=False).index
    )

    print("+----------------+------------+--------------------------+")
    print("| Feature        | Correlation| Interpretation           |")
    print("+----------------+------------+--------------------------+")
    for feature, value in corr.items():
        print(f"| {feature:<14} | {value:>10.6f} | {traduction(value):<24} |")

    print("+----------------+------------+--------------------------+")


def traduction(target):
    tar = abs(target)

    if tar >= 0.7:
        strength = "Strong"
    elif tar >= 0.4:
        strength = "Moderate"
    elif tar >= 0.1:
        strength = "Weak"
    else:
        strength = "Very weak"

    return strength


if __name__ == "__main__":
    correlation()