import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *

home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
prefix = os.path.relpath(home_directory)
address = Address(prefix = prefix)


# Flushing output after printing
def printf(*args):
    print(*args)
    sys.stdout.flush()


# tag_lookup
def tag_lookup(df_tag: pd.DataFrame):
    tag_dict = {}
    for tag_ind, row in df_tag.iterrows():
        tag_dict[row['tags']] = tag_ind
    return tag_dict


# Convert data into numpy array
def problem_df_to_np(df_problem: pd.DataFrame):
    df_tag = pd.read_csv(address.data.tags)
    num_tag = len(df_tag)
    processed_data = []
    tag_dict = tag_lookup(df_tag)
    
    # Creating numpy array of data
    for ind_prob, problem in df_problem.iterrows():
        converted_problem = [problem['difficulty'], problem['points'], problem['rating'], problem['solvedCount']]
        # One Hot Encoding for tags
        converted_problem.extend([0]*num_tag)
        for tag in problem['tags']:
            converted_problem[4 + tag_dict[tag]] = 1
        processed_data.append(converted_problem)
        
    processed_data = np.array(processed_data)
    
    return num_tag, processed_data


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
def create_weight(num_tag = None, weights = None, problem_Data = None):
    if num_tag is None:
        df_tag = pd.read_csv(address.data.tags)
        num_tag = len(df_tag)
    if weights is not None:
        weights = list(weights*num_tag)
    elif problem_Data is None:
        weights =[num_tag, num_tag/530, num_tag/16000, num_tag/1370]
    else:
        imputed_data = SimpleImputer(missing_values=np.nan, strategy='mean').fit_transform(problem_Data)
        weights = np.std(imputed_data[:, :4], axis = 0)
        weights = weights*weights
        prob = np.sum(imputed_data[:, 4:])/(imputed_data.shape[0]*num_tag)
        weights = list(num_tag * prob * (1-prob)/weights)
    weights.extend([1]*num_tag)
    return np.array(weights)
