import streamlit as st
import requests

st.title('Fish weight prediction client app')

st.image("../assets/measure.gif", width=450)

API_URI = "http://localhost:8080/predict"

api_uri = st.text_input("API Endpoint URI", value=API_URI, type="default", help="The URI of the ML server running on, <url>:<port>/predict. May be localhost or any other external url")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

specie = st.selectbox("Specie", ['perch','bream','roach','pike','smelt','parkki','whitefish'], index=1)
length = st.slider("Length", min_value=0.0, max_value=100.0, value=23.9, step=0.1)
height = st.slider("Height", min_value=0.0, max_value=50.0, value=12.3778, step=0.1)
width = st.slider("Width", min_value=0.0, max_value=20.0, value=4.6961, step=0.1)

features = {
  "species": specie,
  "length1": length,
  "height": height,
  "width": width
}

response = requests.post(url=api_uri, json=features)
prediction = response.json()
if isinstance(prediction, list):
    if len(prediction) == 1:
        prediction = prediction[0]
st.header(f"Predicted weight = {prediction}")

