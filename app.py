import os.path
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from function.featureExtraction import featureExtraction


# GLOBAL SETTINGS:
CURRENT_FILE = __file__
F = os.path.dirname(os.path.abspath(CURRENT_FILE))
DATASET_URL = F + r"/data/train.csv"


def preprocessing_DATA():
    data = pd.read_csv(DATASET_URL, sep=",", encoding="utf-8")
    no_label_index = list(
        data.loc[(data['label'] != '1') & (data['label'] != 0) & (data['label'] != '0') & (data['label'] != 1)].index)
    data = data.drop(index=no_label_index)
    data = data.drop(columns=["url", "code", "scheme", "domain", "subdomain", "second_domain", "tld", "url_path", "words_raw"], axis=1)
    data = data.reset_index(drop=True)
    return data


def trainModel(X, y, model_):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X)

    if model_.__name__ == "SVC":
        model = model_(probability=True)
    else:
        model = model_()
    model.fit(X_train, y)
    joblib.dump(model, F + f"/data/models/{model_.__name__}.joblib")


def predictLabel(X, url, model_):
    scaler = StandardScaler()
    scaler.fit(X)
    model = joblib.load(F + f"/data/models/{model_.__name__}.joblib")

    # Predict outcomes on new data
    df = pd.DataFrame()
    df['domain'] = pd.Series(url)
    X_new = featureExtraction(df)
    X_new = X_new.drop(columns=['domain', 'registered_domain', 'https'], axis=1)

    X_new = scaler.transform(X_new)
    probabilities = model.predict_proba(X_new)
    # Get the class with the highest probability for the new data point
    predicted_class_index = probabilities.argmax(axis=1)
    predicted_class_probability = probabilities.max(axis=1) * 100

    # Get 3 important value:
    model_name = model_.__name__
    predicted_class = ('Phishing' if model.classes_[predicted_class_index][0] == 1 else 'Legitimate')
    probability = round(predicted_class_probability[0], 2)

    # Print the predicted class and its probability percentage
    print(f"Algorithm: {model_name}")
    print("Predicted class: " + predicted_class)
    print(f"Probability: {probability}%")
    return model_name, predicted_class, probability


if __name__ == '__main__':
    data = preprocessing_DATA()

    X = data.drop(columns=['label'], axis=1)
    y = data['label'].apply(lambda x: int(x))

    trainModel(X, y, RandomForestClassifier)



