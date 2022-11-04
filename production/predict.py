import pickle
from flask import Flask, request, jsonify
import pandas as pd

from sklearn.base import TransformerMixin, BaseEstimator


MODEL_PATH = '../model/'
MODEL_FILENAME = MODEL_PATH + 'model.pkl'

class ToDictTransformer(TransformerMixin, BaseEstimator):

    def __init__(self):
        self.columns = None

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        return df.to_dict(orient='records')

    def get_feature_names_out(self, *args, **kwargs):
        return self.columns

app = Flask('fish-weight-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():

    fish = request.get_json()
    print(fish)
    prediction = model.predict(pd.DataFrame([fish]))
    print(prediction)
    return jsonify(prediction.tolist())

if __name__ == '__main__':

    with open(MODEL_FILENAME, 'rb') as f_in:
        model = pickle.load(f_in)

    app.run(debug=False, host="0.0.0.0", port=9000)
