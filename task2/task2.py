import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing

cal_housing = fetch_california_housing()
X = pd.DataFrame(cal_housing.data, columns=cal_housing.feature_names)

y = cal_housing.target