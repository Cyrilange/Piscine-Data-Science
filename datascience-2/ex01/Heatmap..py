import matplotlib.pyplot as plt
import pandas as pd

def read_data():
    test = pd.read_csv("../Test_knight.csv")
    train = pd.read_csv("../Train_knight.csv")
    
    return test, train

def get_graph():
    test, train = read_data()

    data = pd.concat([test, train], ignore_index=True)
    data["knight"] = data["knight"].map({"Jedi": 0, "Sith": 1})
    correlation = data.corr(numeric_only=True)
    
    fig, ax = plt.subplots()

    image = ax.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)

    ax.set_xticks(range(len(correlation.columns)))
    ax.set_xticklabels(correlation.columns, rotation=90)

    ax.set_yticks(range(len(correlation.index)))
    ax.set_yticklabels(correlation.index)

    fig.colorbar(image, ax=ax)
    plt.tight_layout()
    plt.show()

def main():
    get_graph()

if __name__ == "__main__":
    main()


#     with no pandas
#         from math import sqrt

# def correlation(x, y):
#     n = len(x)

#     moyenne_x = sum(x) / n
#     moyenne_y = sum(y) / n

#     numerateur = sum(
#         (x[i] - moyenne_x) * (y[i] - moyenne_y)
#         for i in range(n)
#     )

#     sum_x = sum((val - moyenne_x) ** 2 for val in x)
#     sum_y = sum((val - moyenne_y) ** 2 for val in y)

#     denominateur = sqrt(sum_x * sum_y)

#     if denominateur == 0:
#         return 0

#     return numerateur / denominateur


# force = [1, 2, 3, 4, 5]
# vitesse = [2, 4, 6, 8, 10]

# print(correlation(force, speed))