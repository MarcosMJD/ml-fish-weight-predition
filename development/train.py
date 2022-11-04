import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer
from xgboost.sklearn import XGBRegressor
from pathlib import Path


DATASET_PATH = '../data/'
MODEL_PATH = '../model/'
DATASET_FILENAME = DATASET_PATH + 'fish.zip'
MODEL_FILENAME = MODEL_PATH + 'model.pkl'

class ToDictTransformer(TransformerMixin, BaseEstimator):

  def __init__(self):
    self.columns = None

  def fit(self, df, y=None):
    return self

  def transform(self, df):
    return df.to_dict(orient='records')

  def get_feature_names_out(self, *args, **kwargs):
    return self.columns

def remove_outliers(df, columns):
    df = df.copy()
    for column in columns:
        serie = df[column]
        q1 =  serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1
        lower_value = q1 - 1.5 * iqr
        higher_value = q3 + 1.5 * iqr
        to_remove = df[(serie < lower_value) | (serie > higher_value)].index
        """
        if len(to_remove) > 0:
            print('Removing outliers')
            print(to_remove)
        """
        df.drop(to_remove, inplace=True)
    return df

Path(MODEL_PATH).mkdir(parents=True, exist_ok=True)

raw_dataset = pd.read_csv(DATASET_FILENAME)
raw_dataset.columns = raw_dataset.columns.str.lower().str.replace(' ','_')

# Define features and target columns (length2 and length3 are not used)
target = 'weight'
categorical = ['species']
numerical = ['length1', 'height', 'width']

# Delete samples with weight = 0
raw_dataset.drop(raw_dataset[raw_dataset[target] < 1].index, axis=0, inplace=True)
# Remove outliers
dataset = remove_outliers(raw_dataset, numerical)


df_full_train, df_test = train_test_split(raw_dataset, test_size=0.2, random_state=5, stratify=raw_dataset[categorical])
df_train, df_val = train_test_split(raw_dataset, test_size=0.25, random_state=5, stratify=raw_dataset[categorical])

y_full_train = df_full_train[target].values
y_train = df_train[target].values
y_val = df_val[target].values
y_test = df_test[target].values

del df_full_train[target]
del df_train[target]
del df_val[target]
del df_test[target]

categorical_pipeline = make_pipeline(ToDictTransformer(), DictVectorizer())

preprocessor = ColumnTransformer([
  ('categorical', categorical_pipeline, categorical),
  ('numerical', StandardScaler(), numerical)
])

xgboost_best_params = {
    'xgbregressor__eta': 0.1,
    'xgbregressor__max_depth': 5,
    'xgbregressor__min_child_weight': 1,
    'xgbregressor__n_estimators': 80
}
xgb_regressor = XGBRegressor(random_state=5, n_jobs=4)
train_pipeline = make_pipeline(preprocessor, xgb_regressor)
train_pipeline.fit(df_full_train, y_full_train)

y_pred = train_pipeline.predict(df_test)
test_rmse = mean_squared_error(y_pred, y_test, squared=False)
print(f'test_rmse = {test_rmse}')

with open(MODEL_FILENAME, 'wb') as f_out:
    pickle.dump(train_pipeline, f_out)
