import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
import mlflow
from sklearn.pipeline import Pipeline

train_set = pd.read_csv("data/train_sub_set.csv",index_col=0)
test_set = pd.read_csv("data/test_sub_set.csv",index_col=0)

X_train = train_set.drop(["target"], axis=1)
X_test = test_set.drop(["target"], axis=1)
y_train = train_set[["target"]]
y_test = test_set[["target"]]

mlflow.autolog()
with mlflow.start_run():
    # Create Classifier object
    pipe = Pipeline([('scaler', StandardScaler()), ('sgd_clf', SGDClassifier())])
    pipe.fit(X_train, y_train).score(X_test, y_test)

    mlflow.sklearn.log_model(
        pipe,
        "SGDClassifier",
        input_example=X_train,
        code_paths=['train.py','data.py']
    )
    