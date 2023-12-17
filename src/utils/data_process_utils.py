from math import isnan
import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *


# Flushing output after printing
def printf(*args):
    print(*args)
    sys.stdout.flush()


# Distance between two problems
def distance(X, Y, weights, missing_values=np.nan):
    diff = X - Y
    sq_diff = diff * diff
    if np.isnan(missing_values):
        not_missing_index = np.argwhere(~np.isnan(sq_diff))
    else:
        not_missing_index = np.argwhere(sq_diff != missing_values)
    new_weight = weights[not_missing_index]
    new_weight/=np.sum(new_weight)     # Normalizing new weights
    dist = np.matmul(new_weight.T, sq_diff[not_missing_index])
    return dist

def distance_func(weights):
    return lambda X, Y, missing_values: distance(X, Y, weights, missing_values = missing_values)


# Create Weight
def create_weight(num_tag = None, weights = None):
    if weights is not None:
        weights *= num_tag
        weights = list(weights)
    if num_tag is None:
        df_tag = pd.read_csv(address.data.tags)
        num_tag = len(df_tag)
    weights =[num_tag, num_tag/530, num_tag/16000, num_tag/1370]
    weights.extend([1]*num_tag)
    return np.array(weights)
