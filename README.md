# Fish Weight Prediction

ML project to predict the weight of a fish from its dimensions.

## Project description

## Dataset description


## How to run

### Setup
pip install -U pip
pip install pipenv
pipenv install --dev
### Development
jupyter notebook
train.py
serve.py
### Build
docker build
### Deploy
Local
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


# Userful snippets

Remove outliers based on z-score (x-u/s)

import numpy as np
from scipy import stats
df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]



