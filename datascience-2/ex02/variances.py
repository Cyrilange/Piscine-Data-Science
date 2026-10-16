
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def main():
    """
    Read the data.
    Drop the columns not necessary (knight)
    Select the numerical features.
    Standardize the data.
    Apply PCA.
    Calculate and print the explained variance percentages.
    Calculate and print the cumulative explained variance.
    Plot the cumulative explained variance.
    """
    data = pd.read_csv("../Train_knight.csv")
    skills = data.drop(columns=["knight"], errors="ignore")
    skills = skills.select_dtypes(include="number").dropna()
    scaled_data = StandardScaler().fit_transform(skills)
    pca = PCA()
    pca.fit(scaled_data)
    variances = pca.explained_variance_ratio_ * 100
    cumulative = variances.cumsum()

    print("Variances (Percentage):")
    print(variances)

    print("Cumulative Variances (Percentage):")
    print(cumulative)

    n_components = (cumulative < 90).sum() + 1
    print("Number of components needed:", n_components)
    plt.plot(
        range(1, len(cumulative) + 1),
        cumulative,
        marker="o"
    )
    plt.axhline(
        y=90,
        color="red",
        linestyle="-",
        label="90%")
    plt.axvline(
        x=n_components,
        color="green",
        linestyle="-",
        label=f"{n_components} components"
    )

    plt.xlabel("Number of components")
    plt.ylabel("Cumulative variance (%)")
    plt.title("Cumulative explained variance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
