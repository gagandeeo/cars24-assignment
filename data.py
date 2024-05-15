from sklearn.datasets import fetch_openml
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
mnist = fetch_openml('mnist_784', version=1)
data = mnist["data"]
data["target"] = mnist["target"]

train_set = data[:10000]
test_set = data[10000:15000]

train_set.to_csv("data/train_sub_set.csv")
test_set.to_csv("data/test_sub_set.csv")
# The MNIST dataset is actually already split into a training set (the first 60,000 images) and a test set (the last 10,000 images): 
