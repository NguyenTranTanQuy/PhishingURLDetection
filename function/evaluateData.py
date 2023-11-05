import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def evaluateData(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
    accuracy_test = []
    models = [DecisionTreeClassifier, RandomForestClassifier, KNeighborsClassifier, SVC]
    for m in models:
        print('#############################################')
        print('######-Model =>\033[07m {} \033[0m'.format(m))
        model_ = m()
        model_.fit(X_train, y_train)
        predict = model_.predict(X_test)
        acc = accuracy_score(predict, y_test)
        accuracy_test.append(acc)
        print('Test Accuracy :\033[32m \033[01m {:.2f}% \033[30m \033[0m'.format(acc * 100))
        print('\033[01m              Classification_report \033[0m')
        print(classification_report(y_test, predict))
        print('\033[01m             Confusion_matrix \033[0m')
        cf_matrix = confusion_matrix(y_test, predict)
        plot_ = sns.heatmap(cf_matrix / np.sum(cf_matrix), annot=True, fmt='0.2%')
        plt.show()
        print('\033[31m###################- End -###################\033[0m')

    output = pd.DataFrame({"Model": ['Decision Tree Classifier', 'Random Forest Classifier', 'KNeighbors Classifier',
                                     'Support Vector Machine'],
                           "Accuracy": accuracy_test})
    print(output)