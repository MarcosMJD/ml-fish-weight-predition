import requests
import math
from argparse import ArgumentParser

# Bream	340.0	23.9	26.5	31.1	12.3778	4.6961

DEFAULT_URI = 'http://127.0.0.1:8080/predict'

y_true = 340.0

test_data = {
  "species":"bream",
  "length1": 23.9,
  "height": 12.3778,
  "width": 4.6961
}


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "--uri",
        default=DEFAULT_URI,
        help="URL of the service's API endpoint"        
    )

    args = parser.parse_args()

    r = requests.post(args.uri, json=test_data)
    predicted_weight = r.json()[0]
    print(f'Predicted weight = {predicted_weight}')
    rmse = math.sqrt((predicted_weight - y_true)**2)
    print(f'rmse = {rmse}')
