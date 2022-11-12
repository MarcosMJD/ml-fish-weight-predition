# Fish Weight Prediction

Machine Learning project to predict the weight of a fish from its dimensions and specie.

# Project description

The goal is to productionize a web service for the end users that will predict the weight of a fish from its dimensions for 7 different species.  
The project will deal with a dataset which is small and with highly correlated features. The dataset is clean with a few sliders.  

This project uses:

Jupyter
Numpy/Pandas
MatplotLib/Seaborn
Scikit-learn (linear regressors, decision trees, random forest)
XGBoost
Docker
AWS Elastic Beanstalk
AWS ECR
AWS ECS
Streamlit

# Dataset description
This dataset is a record of 7 common different fish species in fish market sales. With this dataset, a predictive model can be performed using machine friendly data and estimate the weight of fish can be predicted.
https://www.kaggle.com/datasets/aungpyaeap/fish-market

- Size: 159 records
- 7 columns
- Decimal: 6
- String: 1
- Species: species name of fish
- Weight: weight of fish in Gram g
- Length1: vertical length in cm
- Length2: diagonal length in cm
- Length3: cross length in cm
- Height: height in cm
- Width: diagonal width in cm

 ![measures](/assets/measure.gif)

# How to run

## Clone the repo

git clone https://github.com/MarcosMJD/ml-fish-weight-predition.git

## Setup
It is recommended to install Anaconda or miniconda. The project has been developed with:
- Anaconda (as the default framework, although in this particular project, only is used to get the python interpreter...)  
- Visual Studio Code  
- Windows 10  
- git and GitBash.  

You can use your own OS/python version manager. It is required python=3.9  

Open a shell (GitBash, bash or Powershell) and execute the following instructions:

Create a conda environment (recommended):  
In the root directory of the repository, execute:  
`conda create --name py39 python=3.9`  
`conda activate py39` 
Install pip and pipenv  
`pip install -U pip` alternatively `python.exe -m pip install -U pip`  
`pip install pipenv`     
Create the environment and install dependencies    
`pipenv install --dev`  
Activate the environment  
`pipenv shell`    

## Development  

**jupyter notebook**  
Start jupyter notebook with
`jupyter notebook`  

Go the browser and open `./development/notebook.ipynb`   
Run all cells check the EDA, tranning of models, model evaluation and model selection.    

**Trainning script**  
In the development directory, execute the trainning script:  
`python train.py`  
The best model with best parameters will be saved into the model directory. 
Two models are saved. One is the standard way with pickle.
The other is with BentoML. This model will be stored under your home path / bentoml directory.  

## Production service  
The script predict.py will be used to receive the features and make the predictions.  
Flask is used as the application server.   
Waitress is used as the WSGI.  
In Linux or MacOS, gunicorn may be used as well.    

**Local test**  
Under production directory, start the server with:  
`waitress-serve predict:app`  
Do not worry about the warning message, this is not a concern, since we are using waitress as the WSGI server  
You can test the service with the script (local_test.py), running on another shell.
Execute the test script in a new shell:  
`conda activate py39`  
`pipenv shell`  
`cd ./production`  
`python test.py`  
The prediction shall be:  
Predicted weight = 335.184326171875  
rmse = 4.815673828125  

You can parametrize uri:
`python test.py --uri http://127.0.0.1:8080/predict`

## Build the service
The model and prediction script will be containerized.  

Go to the root directory of the project  
`docker build --tag ml-fish-weight-prediction:latest .`   

Note about Dockerfile
entrypoint = start.sh. This script will change the directory to ./production.  
This is needed to allow production.py to find the model in the right directory.  
WARNING! Is you edit start.sh in Windows, change CRLF to LF.  

**Local test**
Run the container:  
`docker run --rm -p 8080:8080 ml-fish-weight-prediction:latest`  
Execute the test script in a new shell:  

`conda activate py39`  
`pipenv shell`  
`cd ./production`  
`python test.py`

Test again:  
`python test.py --uri http://127.0.0.1:8080/predict`

## Deployment
Temporarily, you can find the service running on http://34.240.92.102:3000/ on AWS ECS. If it does not work, please, launch your own deployment with the instructions below  
Test it with:  
`python test.py --uri http://34.240.92.102:3000/predict`
Or with:
`streamlit run client.py`
on the production subdirectory. Also, configure the URI acordingly.  

## Deployment with Elastic Beanstalk

The service is deployed with AWS Elastic Beanstalk in the following url:

If you wish to deploy your own service, follow these instructions:  

Setup AWS account:  
Follow the instructions in this article: https://mlbookcamp.com/article/aws  

Go to the root directory of the project:    
`pipenv install --dev awsebcli`  
Create EB application (use your AWS region)  
`eb init -p docker -r eu-west-1 fish-weight-prediction`    
Test locally with:   
`eb local run --port 8080`  
Use test.py again:  
`python test.py --uri http://127.0.0.1:8080/predict`  
Create EB environment  
**IMPORTANT WARNING**: If you use Windows, you will have to set autocrlf in the local repo to false. It is needed in order to keep LF when pushing the files to EB.  
`git config core.autocrlf false`  
Create the EB environment:  
`eb create fish-weight-prediction-env`  
Copy the url after "Application available at"  
and use in the call to `test.py`  
Run the escript `eb_test.py`  
`python test.py --uri http://<your-url>:8080/predict`   
`eb terminate`   

## Build the service with BentoML

The script predict_bento.py will use BentoML to serve the service. This script will load the saved model in BentoML format.  
Under the production directory, execute:  
`bentoml serve .\predict_bento.py:svc --reload`  
Test with: `python test.py --uri http://127.0.0.1:3000/predict`  
You can also test the swagger ui (automatically generated from the openapi spec generated by BentoML)  
Just follow the local URL listed when running bento serve (in Windows, use 127.0.0.1 for the local IP address)  
Use this features as an example (just click on the POST / predict endpoint and try it out)  
```
{
  "species":"bream",
  "length1": 23.9,
  "height": 12.3778,
  "width": 4.6961
}
```

Build the bento:
This will pack all the files needed to serve the service with BentoML   
`bentoml build`  
Keep the tag.

**Note: Change the tag accordingly in the following instructions**.

Create the Docker image:  
`bentoml containerize fish_weight_prediction:a4fyykc7pcmy7sda`. 

Run and test locally:
`docker run -it --rm -p 3000:3000 fish_weight_prediction:y7dnw7c7og4bnsda serve --production`  
`python test.py --uri http://127.0.0.1:3000/predict` 
You can also test the Swagger UI.  

## Deploy the service with BentoML and AWS ECR, ECS
To deploy, let's use ECR and ECS:  
Go to AWS Console and create an ECR called fish-weight-prediction. Follow this video: https://youtu.be/aF-TfJXQX-w?t=208

Log into ECR with aws cli (change your account id and region accordingly):   
`aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com`

Tag the recently created image:  
`docker tag fish_weight_prediction:y7dnw7c7og4bnsda 546106488772.dkr.ecr.eu-west-1.amazonaws.com/fish-weight-prediction:latest`  

Push the image to the ECR registry:  
`docker push 546106488772.dkr.ecr.eu-west-1.amazonaws.com/fish-weight-prediction`  

Create an ECR cluster by following this video:  https://youtu.be/aF-TfJXQX-w?t=514  
Once the ECR cluster and task is created and the task is running, the service will be found in the public ip and port used. You can find this information under the running task information page (on the network section).  
You can test with test.py (do not forget to change use the uri param accordingly)  
Or directly, in the Swagger UI

## Interactive test
In your local machine, under production directory, run `streamlit run .\client.py` and have test you can change the URI of the API endpoint as needed.

# Definitions

R2 score (coefficient of determination)
  It is the proportion of the variance in the dependent variable that is predictable from the independent variable(s).
0-100%
R2 score equals the square of the Pearson correlation coefficient between the observed y and modeled y_pred
pearson (y,y_pred) = cov(y,y_pred) / sy sy_pred
cov = 1/n (sum (x-mean(x))(y-mean(y)))

1 - (SSred/SStot)
SSred = sum(y-ypred)**2
SStot = sum(y-mean(y))**2

# Notes

About WSGI  
https://python-docs.readthedocs.io/en/latest/scenarios/web.html

Crossvalidation cross_val_score  
When the cv argument is an integer, cross_val_score uses the KFold or StratifiedKFold strategies by default, the latter being used if the estimator derives from ClassifierMixin.

Why regularization needs standardization  
If the independent variables are of different scale then penalty parameter will have a different impact on these variable coefficients and this would result in unfair shrinking since the penalized term is nothing but the sum of square of all coefficients. Hence to avoid this problem of unfair shrinking we standardize our input variable matrix in order to have variance 1.

Lasso: 
When the dataset includes collinear features, Lasso regression is unstable in a similar way as unregularized linear models are, meaning that the coefficients (and thus feature ranks) can vary significantly even on small data changes.
The Lasso regression not only penalizes the high β values but it also converges the irrelevant variable coefficients to 0. Therefore, we end up getting fewer variables which in turn has higher advantage.
Can be used for dimension reduction and feature selection

Ridge:
Higher the value of λ, greater will be the shrinkage of the β coefficients and this, in turn, makes the coefficients more robust to collinearity. Coefficients converge to 0 but does not make their value 0. This means that Ridge regression will not enforce the irrelevant variable coefficients to become 0 rather, it will reduce the impact of these variables on the model.
Can be user when we have collinear features

# Useful snippets

Remove outliers based on z-score (x-u/s)  

```
import numpy as np  
from scipy import stats
df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
```

Enable conda in powershell.  
`powershell -executionpolicy remotesigned`  
or in a powershell: `set-executionpolicy remotesigned`  
To check:  
`get-executionpolicy` (default is restricted)  
