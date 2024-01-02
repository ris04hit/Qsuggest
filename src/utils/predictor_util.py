import sys
import os
import numpy as np
import pandas as pd
import torch
import asyncio
from sklearn.impute import KNNImputer

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.scrape_utils import *
from utils.data_process_utils import *
from models.up_probability_model import predict

home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
prefix = os.path.relpath(home_directory)
address = Address(prefix = prefix)

# Creating data for particular user
def create_user_data(handle: str, problem_class: np.ndarray, database = False, user_info = None, submission = None):
    num_class = len(set(problem_class))
    
    if database:        # Extracting data from database
        df_user = pd.read_csv(address.data.handles)
        user = df_user[df_user['handle'] == handle]
        
        df_submission = pd.read_csv(address.data.submission(handle))
        df_submission = df_submission[df_submission['verdict'] == 'OK']
        
        problemId = set(df_submission['problemId'])
    
    else:              # Extracting data from codeforces API
        if user_info is None:
            user = asyncio.run(get_user_info(handle))
        else:
            user = user_info
        
        if submission is None:
            df_submission = pd.DataFrame(asyncio.run(get_user_submission(handle)))
        else:
            df_submission = pd.DataFrame(submission)
        df_solved_problems = df_submission[df_submission['verdict'] == 'OK']['problem'].apply(pd.Series)
        
        df_problem = pd.read_csv(address.data.problems)
        problemId_lookup_func = problemId_lookup(df_problem)
        problemId_df = df_solved_problems.apply(problemId_lookup_func, axis=1).dropna().astype(int)
        problemId = set(problemId_df)
        
        print("Fetched Data from Codeforces")
    
    onehot_class = np.zeros((num_class, ))
    for pid in problemId:
        onehot_class[problem_class[pid]] += 1
        
    return np.insert(onehot_class, 0, user['rating']), problemId
        

# Create data for prediction (changes problem_data)
def create_prediction_data(handle: str, problem_class: np.ndarray, problem_data: np.ndarray, up_stat, database = False, user_info = None, submission = None):
    def increment_func(user_data, index):
        new_user_data = np.copy(user_data)
        if (index != 0):
            new_user_data[index] += 1
        return new_user_data
    
    # Creating user data
    user_data, solved_problem = create_user_data(handle, problem_class, database, user_info, submission)
    index_arr = np.arange(user_data.shape[0]).reshape((-1, 1))
    user_data_table = np.apply_along_axis(lambda index: increment_func(user_data, index), axis = 1, arr = index_arr)
    user_data_width = user_data_table.shape[1]
    
    # stats data
    shape_arr = up_stat['length']
    mean_arr = up_stat['mean']
    std_arr = up_stat['std']
    cont_inp_width = shape_arr[0][1]
    
    print("Created user and problem data")
    
    # Normalize data
    user_data_table -= mean_arr[:, :user_data_width]
    problem_data[:, :cont_inp_width-user_data_width] -= mean_arr[:, user_data_width:]
    np.seterr(invalid='ignore')
    user_data_table = np.nan_to_num(np.divide(user_data_table,
                                              std_arr[:, :user_data_width],
                                              out = np.zeros_like(user_data_table),
                                              where = std_arr[:, :user_data_width]!=0))
    problem_data[:, :cont_inp_width-user_data_width] = np.nan_to_num(np.divide(problem_data[:, :cont_inp_width-user_data_width],
                                                                               std_arr[:, user_data_width:],
                                                                               out = np.zeros_like(problem_data[:, :cont_inp_width-user_data_width]),
                                                                               where = std_arr[:, user_data_width:]!=0))
    np.seterr(invalid='warn')
    
    print("Normalized Data")
    
    return user_data_table, problem_data, solved_problem


# Calculates probabilistic advantage
def prob_advantage(handle, database = False, user_info = None, submission = None):
    def predict_local(user, problem_data):
        concat_data = np.apply_along_axis(lambda problem: np.concatenate((user, problem)), axis = 1, arr = problem_data)
        return predict(torch.Tensor(concat_data.astype(np.float64))).to('cpu').detach().numpy()[:, 0]
    
    # Problem class data
    problem_class = np.load(address.data.problem_class)
    num_class = len(set(problem_class))
    
    # Problem data
    problem_data = np.load(address.data.imputed_prob)
    num_problem = problem_data.shape[0]
    
    # Loading stats data
    up_stat = np.load(address.data.user_problem_stat)
    
    # Prediction data
    user_data, problem_data, solved_problem = create_prediction_data(handle, problem_class, problem_data, up_stat, database, user_info, submission)
    
    # Probability data
    prob_data = np.apply_along_axis(lambda user: predict_local(user, problem_data), axis = 1, arr = user_data)
    print("Prediction done by model")
    base_probability = np.copy(prob_data[0])
    
    # Weight for calculating weighted mean
    gamma = 0.999      # Discount Factor for preferring new questions over older questions
    weights = np.geomspace(1, gamma**(num_problem-1), num_problem)
    weights /= np.sum(weights)
    
    # Calculating weighted mean of probability
    prob_data = np.matmul(prob_data, weights.reshape(-1, 1)).flatten()

    # Calculating advantage
    advantage = (prob_data - prob_data[0])[1:]
    
    # Calculating probabilistic advantage
    prob_adv = advantage[problem_class] * base_probability * weights        # multiplying with weights to ensure more weight to new problems
    
    # Ensuring less difficult problems are given
    prob_threshold = 0.5
    difficulty_factor = 0.5
    prob_adv[base_probability < prob_threshold] *= difficulty_factor
    
    return prob_adv, solved_problem


# Caclulates probability of single user/problem
def prob_single(handle, problem, database = False, user_info = None, submission = None):
    # Problem class data
    problem_class = np.load(address.data.problem_class)
    num_class = len(set(problem_class))
    
    # Problem data
    df_problem = pd.read_csv(address.data.problems)
    problem_data = np.load(address.data.imputed_prob)
    num_problem = problem_data.shape[0]
    
    # Loading stats data
    up_stat = np.load(address.data.user_problem_stat)
    shape_arr = up_stat['length']
    mean_arr = up_stat['mean']
    std_arr = up_stat['std']
    cont_inp_width = shape_arr[0][1]
    
    # Prediction data
    user_data, solved_problems = create_user_data(handle, problem_class, database, user_info, submission)
    problemId = problemId_lookup(df_problem)(problem)
    problem_val = problem_data[problemId]
    
    # Checking is problem is in database
    if problemId is None:
        new_problem_df = pd.DataFrame([problem])
        num_tag, problem_val = problem_df_to_np(new_problem_df)
        problem_val[problem_val < 0] = np.nan
        weights = create_weight(num_tag=num_tag, problem_Data=problem_data)
        neigh = KNNImputer(n_neighbors=6, missing_values=np.nan, metric=distance_func(weights)).fit(problem_data)
        problem_val = neigh.transform(problem_val)[0]
    
    # Normalization
    data = np.concatenate((user_data, problem_val)).reshape((1,-1))
    np.seterr(invalid='ignore')
    data[:, :cont_inp_width] -= mean_arr
    data[:, :cont_inp_width] = np.nan_to_num(np.divide(data[:, :cont_inp_width], std_arr, out=np.zeros_like(data[:, :cont_inp_width]), where= std_arr!=0))
    np.seterr(invalid='warn')
    
    # Prediction
    probability = predict(torch.Tensor(data.astype(np.float64))).to('cpu').detach().numpy()[0, 0]
    
    return float(probability)
