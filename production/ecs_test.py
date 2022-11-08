import requests
import math

# Bream	340.0	23.9	26.5	31.1	12.3778	4.6961

URL = "http://176.34.206.194:3000/predict"

y_true = 340.0

test_data = {
  "species":"bream",
  "length1": 23.9,
  "height": 12.3778,
  "width": 4.6961
}

if __name__ == "__main__":

    r = requests.post(URL, json=test_data)

    predicted_weight = r.json()[0]
    print(f'Predicted weight = {predicted_weight}')
    rmse = math.sqrt((predicted_weight - y_true)**2)
    print(f'rmse = {rmse}')

