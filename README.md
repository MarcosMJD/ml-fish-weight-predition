# Fish Weight Prediction

Machine Learning project to predict the weight of a fish from its dimensions and specie.

## Project description

The goal is to productionize a web service for the end users that will predict the weight of a fish from its dimensions for 7 different species.

## Dataset description
This dataset is a record of 7 common different fish species in fish market sales. With this dataset, a predictive model can be performed using machine friendly data and estimate the weight of fish can be predicted.
https://www.kaggle.com/datasets/aungpyaeap/fish-market

Size: 159 records
7 columns
Decimal: 6
String: 1
Species: species name of fish
Weight: weight of fish in Gram g
Length1: vertical length in cm
Length2: diagonal length in cm
Length3: cross length in cm
Height: height in cm
Width: diagonal width in cm

## How to run

### Clone the repo

git clone https://github.com/MarcosMJD/ml-fish-weight-predition.git

### Setup
It is recommended to install Anaconda or miniconda. The project has been developed with:
- Anaconda (as the default framework, although in this particular project, only is used to get the python interpreter...)  
- Visual Studio Code  
- Windows 10  
- git and GitBash.  

You can use your own OS/python version manager. It is required python=3.9  

Open a shell (GitBash, bash or Powershell) and execute the following instructions:

Create a conda environment:  
In the root directory of the repository, execute:
`conda create --name py39 python=3.9`  
`conda activate py39` 
Install pip and pipenv  
`pip install -U pip`   
`pip install pipenv`   
Create the environment and install dependencies  
`pipenv install --dev`  
Activate the environment  
`pipenv shell`    

### Development  

**jupyter notebook**  
Start jupyter notebook with
`jupyter notebook`

Go the browser and open `./development/notebook.ipynb`  
Run all cells check the EDA, tranning of models, model evaluation and model selection.    

**Trainning script**
Go to the production directory and execute the trainning script:  
`cd production`
`python train.py`
The model will be saved into the model directory.  

### Prediction service
The script predict.py will be used to receive the features and make the prediction.
Flask and gunicorn will are used.  

**Local test**
You can test the service with the following script.
`python local_test.py`

### Build
The model and prediction script will be containerized.  

Go to the root directory of the project  
`docker build --tag ml-fish-weight-prediction:latest .`  

**Local test**
Run the container:  
`docker run --rm -p 9000:9000 ml-fish-weight-prediction:latest ` 
Execute the test script in a new shell:  

`conda activate py39`  
`pipenv shell`  
`cd ./production`  
`python local_test.py`

### Deployment

To cloud. 

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

When the cv argument is an integer, cross_val_score uses the KFold or StratifiedKFold strategies by default, the latter being used if the estimator derives from ClassifierMixin.

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

import numpy as np
from scipy import stats
df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]


Enable conda in powershell. 
powershell -executionpolicy remotesigned
or in a powershell: set-executionpolicy remotesigned
To check:
get-executionpolicy (default is restricted)