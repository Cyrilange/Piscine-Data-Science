
import pandas as pd

def pourcent_find():
    df = pd.read_csv("../Train_knight.csv")
    training = df.sample(frac=0.8, random_state=42)
    all_indexes = df.index
    training_indexes = training.index
    remaining_indexes = all_indexes.difference(training_indexes)
    validation = df.loc[remaining_indexes]
    training.to_csv("Training_knight.csv", index=False)
    validation.to_csv("Validation_knight.csv", index=False)
    print("Nombre de lignes total :", len(df))
    print("Training :", len(training))
    print("Validation :", len(validation))


if __name__ == "__main__":
    pourcent_find()
