from sklearn.base import TransformerMixin, BaseEstimator

class ToDictTransformer(TransformerMixin, BaseEstimator):

  def __init__(self):
    self.columns = None

  def fit(self, df, y=None):
    return self

  def transform(self, df):
    return df.to_dict(orient='records')

  def get_feature_names_out(self, *args, **kwargs):
    return self.columns