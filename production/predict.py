import pickle
from flask import Flask, request, jsonify
import pandas as pd
from dict_vect_transformer import ToDictTransformer

MODEL_PATH = '../model/'
MODEL_FILENAME = MODEL_PATH + 'model.pkl'

app = Flask('fish-weight-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():

    fish = request.get_json()
    print(fish)
    prediction = model.predict(pd.DataFrame([fish]))
    print(prediction)
    return jsonify(prediction.tolist())

with open(MODEL_FILENAME, 'rb') as f_in:
    model = pickle.load(f_in)

app.run(debug=False, host="0.0.0.0", port=8080)

if __name__ == '__main__':

    with open(MODEL_FILENAME, 'rb') as f_in:
        model = pickle.load(f_in)

    app.run(debug=False, host="0.0.0.0", port=9000)



