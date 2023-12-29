import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
import time

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *

home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
prefix = os.path.relpath(home_directory)
address = Address(prefix = prefix)


# Flushing output after printing
def printf(*args):
    print(*args)
    sys.stdout.flush()


# Incorporates ratings to submissions
def update_submission(handle: str, df_ratings: pd.DataFrame, overwrite: bool):
    df_submission = pd.read_csv(address.data.submission(handle))
    if overwrite or ('rating' not in df_submission):
        new_rating = 0
        rating_list = []
        rating_ind = -1
        for ind_submission, row_submission in df_submission[::-1].iterrows():
            submit_time = row_submission['creationTimeSeconds']
            while (rating_ind < len(df_ratings)-1) and (df_ratings['ratingUpdateTimeSeconds'][rating_ind+1] < submit_time):
                rating_ind += 1
                new_rating = df_ratings['newRating'][rating_ind]
            rating_list.append(new_rating)
        rating_list.reverse()
        df_submission['rating'] = rating_list
        df_submission.to_csv(address.data.submission(handle), index = False)


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
        converted_problem = [1000*problem['difficulty'], problem['points'], problem['rating'], problem['solvedCount']/100]
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


# Getting unique elements from list without altering the order
def get_unique_elements(input_list):
    unique_elements = set()
    result = []

    for item in input_list:
        if item not in unique_elements:
            result.append(item)
            unique_elements.add(item)

    return result


# Calculates probability for a df
def prob_calc(df: pd.DataFrame, problem_class: np.ndarray):
    df = df.reset_index(drop=True)
    problemId = df['problemId'][0]
    rating = df['rating'][0]
    label = problem_class[problemId]
    
    # Calculating probability
    num_attempt = len(df)
    num_correct = (df['verdict'] == 'OK').sum()
    solve_probability = (num_correct > 0)*(1/(num_attempt - num_correct + 1))
    
    # Creating pd series
    return pd.Series({'problemId': problemId,
                        'prob_class': label,
                        'rating': rating,
                        'solve_prob': solve_probability})


# Creating data for a particular user problem
def create_up_data(user: pd.Series, problem_class: np.ndarray, problem_data: np.ndarray, num_tag: int, start_time = time.time()):
    num_class = len(set(problem_class))
    df_submission = pd.read_csv(address.data.submission(user['handle']))[['verdict', 'problemId', 'rating']]
    
    # Grouping data based to find prob of each problem
    df_submission['group'] = ((df_submission['problemId'] != df_submission['problemId'].shift(1)) |\
        (df_submission['rating'] != df_submission['rating'].shift(1))).astype(int).cumsum()
    df_grouped = df_submission.groupby('group').apply(lambda grp: prob_calc(grp, problem_class))
    
    # Converting user problem solved in one hot encoding
    onehot_class = np.zeros((len(df_grouped), num_class))
    for class_val in range(num_class):
        onehot_class[:, class_val] = ((df_grouped['prob_class'] == class_val) &\
            (df_grouped['solve_prob'] > 0))[::-1].astype(int).cumsum()
    onehot_class = np.concatenate((np.zeros((1, num_class)), onehot_class[:-1, :]))[::-1]
    
    # Converting df_grouped in np array
    problem_arr = problem_data[df_grouped['problemId'].astype(int).values]
        
    X_arr = np.concatenate((np.array(df_grouped['rating']).reshape((-1, 1)), onehot_class, problem_arr), axis=1)
    Y_arr = np.array([df_grouped['solve_prob'], 1-df_grouped['solve_prob']]).T
    
    printf(f'Processed user {user.name} with handle {user["handle"]}\tTime Taken: {time.time() - start_time}')
    
    with np.errstate(over='ignore'):
        return pd.Series({'x_cont': X_arr[:, :-num_tag].astype(np.float16),
                          'x_cat': X_arr[:, -num_tag:].astype(np.int8),
                          'y': Y_arr.astype(np.float32)})
