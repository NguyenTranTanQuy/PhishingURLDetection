import os.path
import joblib
import pandas as pd
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from function.featureExtraction import featureExtraction


# GLOBAL SETTINGS:
CURRENT_FILE = __file__
F = os.path.dirname(os.path.abspath(CURRENT_FILE))
DATASET_URL = F + r"/data/urlset.csv"
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/data', methods=['POST'])
def get_data():
    model_name = predicted_class = probability = ""
    try:
        data = request.get_json()
        url = data['url']
        data = pd.read_csv(F + '/data/train.csv', sep=",", encoding="utf-8", index_col=False)
        X = data.drop(columns=['domain', 'label', 'registered_domain'], axis=1)
        model_name, predicted_class, probability = predictLabel(X, url, RandomForestClassifier)
        return jsonify({'messenger': predicted_class,
                        "probability": str(probability) + "%"}), 200
    except Exception as e:
        # Print specific error information
        print(f"An error occurred: {str(e)}")

        # Optionally, print the traceback
        import traceback
        traceback.print_exc()

        return jsonify({'messenger': str(e),
                        "probability": "Error"}), 500


@app.route('/api/evaluatedData', methods=['POST'])
def add_data():
    model_name = predicted_class = probability = ""
    try:
        data = request.get_json()
        url = data['url']
        data = pd.read_csv(F + '/data/train.csv', sep=",", encoding="utf-8", index_col=False)
        X = data.drop(columns=['domain', 'label', 'registered_domain'], axis=1)
        model_name, predicted_class, probability = predictLabel(X, url, RandomForestClassifier)
        predicted_class = 0 if predicted_class == 'Phishing' else 1
        with open('./data/evaluatedData.csv', 'a') as csv_file:
            csv_file.write(url + "," + str(predicted_class) + "\n")
        return jsonify({'message': 'Data added to CSV successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def preprocessing_DATA():
    data = pd.read_csv(DATASET_URL, sep=";", encoding="latin1")
    no_label_index = list(
        data.loc[(data['label'] != '1') & (data['label'] != 0) & (data['label'] != '0') & (data['label'] != 1)].index)
    data = data.drop(index=no_label_index)
    data = data.drop(columns=['ranking', 'mld_res', 'mld.ps_res', 'card_rem', 'ratio_Rrem', 'ratio_Arem',
                              'jaccard_RR', 'jaccard_RA', 'jaccard_AR', 'jaccard_AA', 'jaccard_ARrd', 'jaccard_ARrem'], axis=1)
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

    joblib.dump(model, F + f"/data/models/{model_.__name__}.model")


def predictLabel(X, url, model_):
    scaler = StandardScaler()
    scaler.fit_transform(X)
    model = joblib.load(F + f"/data/models/{model_.__name__}.model")

    # Predict outcomes on new data
    df = pd.DataFrame()
    df['domain'] = pd.Series(url)
    X_new = featureExtraction(df)
    X_new = X_new.drop(columns=['domain', 'registered_domain'], axis=1)

    X_new = scaler.transform(X_new)
    probabilities = model.predict_proba(X_new)
    # Get the class with the highest probability for the new data point
    predicted_class_index = probabilities.argmax(axis=1)
    predicted_class_probability = probabilities.max(axis=1) * 100

    # Get 3 important value:
    model_name = model_.__name__
    predicted_class = ('Phishing' if model.classes_[predicted_class_index][0] == 0 else 'Legitimate')
    probability = round(predicted_class_probability[0], 2)

    # Print the predicted class and its probability percentage
    print(f"Algorithm: {model_name}")
    print("Predicted class: " + predicted_class)
    print(f"Probability: {probability}%")
    return model_name, predicted_class, probability


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)