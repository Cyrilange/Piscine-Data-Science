import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant


def calculate_vif(skills):
    skills = add_constant(skills)

    vif_data = pd.DataFrame()
    vif_data["Feature"] = skills.columns
    vif_data["VIF"] = [
        variance_inflation_factor(skills.values, i)
        for i in range(len(skills.columns))
    ]

    vif_data = vif_data[vif_data["Feature"] != "const"].copy()
    vif_data["Tolerance"] = 1 / vif_data["VIF"]

    return vif_data

def select_features(skills):
    while True:
        vif_data = calculate_vif(skills)

        max_vif = vif_data["VIF"].max()

        if max_vif < 5:
            break

        feature_to_remove = vif_data.loc[
            vif_data["VIF"].idxmax(), "Feature"
        ]

        print(f"Removing {feature_to_remove}: VIF = {max_vif:.2f}")
        skills = skills.drop(columns=[feature_to_remove])

    return skills, calculate_vif(skills)


def main():
    """
    Calculate the Variance Inflation Factor (VIF) for each feature.

    Read the CSV file.
    Remove columns that are not skills.
    Calculate and display the VIF and tolerance for each feature.
    Remove features with a VIF greater than or equal to 5.
    Recalculate the VIF after each removal.
    Display the remaining features.
    """
    data = pd.read_csv("../Train_knight.csv")
    skills = data.drop(columns=["knight"], errors="ignore")
    skills = skills.select_dtypes(include="number").dropna()

    selected_skills, final_vif = select_features(skills)

    print("\nVIF:")
    print(final_vif)

    print("\nSelected features:")
    print(selected_skills.columns.tolist())


if __name__ == "__main__":
    main()