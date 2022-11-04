FROM python:3.9.15-slim

RUN pip install -I pip
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

COPY ["./production/predict.py", "./production/"]
COPY ["./model/model.pkl", "./model"]

EXPOSE 9000

ENTRYPOINT [ "python", "./production/predict.py" ]
