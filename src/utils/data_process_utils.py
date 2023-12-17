from math import isnan
import sys
import numpy as np

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