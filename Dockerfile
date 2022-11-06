FROM python:3.9.15-slim

RUN pip install -I pip
RUN pip install pipenv


WORKDIR '/app'

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

COPY ["./production/predict.py", "./production/dict_vect_transformer.py", "./production/start.sh", "./production/"]
COPY ["./model/model.pkl", "./model/"]

EXPOSE 8080

# Running entrypoint = python ./production/predict.py, will make the working directory to be ./app
# hence, the predict.py script will not find the model in the path ../model/ 
# To fix this, use entrypoint = start.sh. This script will change the directory to ./production 
ENTRYPOINT [ "sh", "./production/start.sh" ]
