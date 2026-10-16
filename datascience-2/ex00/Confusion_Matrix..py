import matplotlib.pyplot as plt

def open_and_read():
    docs_txt = ["../truth.txt", "../predictions.txt"]
    data_for_txt = {}

    for name in docs_txt:
        with open(name, "r", encoding="utf-8") as docs:
            data_for_txt[name] = docs.read().splitlines()

    truth = data_for_txt["../truth.txt"]
    predictions = data_for_txt["../predictions.txt"]

    jedi_correct = 0
    jedi_for_sith = 0
    sith_for_jedi = 0
    sith_correct = 0

    for i in range(len(truth)):
        reel = truth[i]
        predict = predictions[i]

        if reel == "Jedi" and predict == "Jedi":
            jedi_correct += 1
        elif reel == "Jedi" and predict == "Sith":
            jedi_for_sith += 1
        elif reel == "Sith" and predict == "Jedi":
            sith_for_jedi += 1
        elif reel == "Sith" and predict == "Sith":
            sith_correct += 1

    # print("Jed i correctly reconised :", jedi_correct)
    # print("Jedi taken for a Sith :", jedi_for_sith)
    # print("Sith taken for a Jedi :", sith_for_jedi)
    # print("Sith correctly reconised :", sith_correct)

    return [[jedi_correct, jedi_for_sith],
        [sith_for_jedi, sith_correct]]



        
def precision(matrix):
    jedi = matrix[0][0] / (matrix[0][0] + matrix[1][0])
    sith = matrix[1][1] / (matrix[0][1] + matrix[1][1])
    return jedi, sith
    
def recall(matrix):
    jedi = matrix[0][0] / sum(matrix[0])
    sith = matrix[1][1] / sum(matrix[1])
    return jedi, sith
    
def fi_score(precision_values, recall_values):
    jedi = 2 * precision_values[0] * recall_values[0] / (
        precision_values[0] + recall_values[0]
    )
    sith = 2 * precision_values[1] * recall_values[1] / (
        precision_values[1] + recall_values[1]
    )
    return jedi, sith
    
def total(matrix):
    jedi = sum(matrix[0])
    sith = sum(matrix[1])
    accuracy = (matrix[0][0] + matrix[1][1]) / (jedi + sith)
    return jedi, sith, accuracy
    

import matplotlib.pyplot as plt
import numpy as np

def graph_made(matrix): 
    fig, ax = plt.subplots()

    image = ax.imshow(matrix, cmap="viridis", vmin=21, vmax=30)

    ax.set_xticks([0, 1])     #ax.set_xticks([0, 1], labels=["Jedi", "Sith"])
    ax.set_yticks([0, 1])     #ax.set_yticks([0, 1], labels=["Jedi", "Sith"])

    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i][j]),
                    ha="center", va="center", color="white")

    fig.colorbar(image, ax=ax)
    plt.show()

    
def main():
    matrix = open_and_read()

    precisions = precision(matrix)
    recalls = recall(matrix)
    f1 = fi_score(precisions, recalls)
    jedi_total, sith_total, accuracy = total(matrix)
    print()
    print("       precision recall f1-score total")
    print()
    print(f"Jedi        {precisions[0]:.2f}   {recalls[0]:.2f}      {f1[0]:.2f}   {jedi_total}")
    print(f"Sith        {precisions[1]:.2f}   {recalls[1]:.2f}      {f1[1]:.2f}   {sith_total}")
    print()
    print(f"accuracy                     {accuracy:.2f}   {jedi_total + sith_total}")
    print()
    print(f"[[{matrix[0][0]} {matrix[0][1]}]")
    print(f"[{matrix[1][0]} {matrix[1][1]}]]")
    graph_made(matrix)


if __name__ == "__main__":
    main()