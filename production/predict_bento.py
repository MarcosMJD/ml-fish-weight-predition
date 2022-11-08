import bentoml
from bentoml.io import JSON
import pandas as pd

model_ref = bentoml.sklearn.get('model_bento:latest')

model_runner = model_ref.to_runner()

svc = bentoml.Service("fish_weight_prediction", runners=[model_runner])

@svc.api(input=JSON(), output=JSON())
def predict(application_data):
    prediction = model_runner.predict.run(pd.DataFrame([application_data]))
    print(prediction)
    return prediction

