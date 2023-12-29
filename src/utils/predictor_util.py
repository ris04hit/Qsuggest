import sys
import os
import numpy as np
import pandas as pd
import torch
import asyncio

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.scrape_utils import *
from models.up_probability_model import predict

home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
prefix = os.path.relpath(home_directory)
address = Address(prefix = prefix)

# Creating data for particular user
def create_user_data(handle: str, problem_class: np.ndarray, database = False):
    num_class = len(set(problem_class))
    
    if database:        # Extracting data from database
        df_user = pd.read_csv(address.data.handles)
        user = df_user[df_user['handle'] == handle]
        
        df_submission = pd.read_csv(address.data.submission(handle))
        df_submission = df_submission[df_submission['verdict'] == 'OK']
        
        problemId = set(df_submission['problemId'])
    
    else:              # Extracting data from codeforces API
        user = asyncio.run(get_user_info(handle))
        
        df_submission = pd.DataFrame(asyncio.run(get_user_submission(handle)))
        df_solved_problems = df_submission[df_submission['verdict'] == 'OK']['problem'].apply(pd.Series)
        
        df_problem = pd.read_csv(address.data.problems)
        problemId_lookup_func = problemId_lookup(df_problem)
        problemId_df = df_solved_problems.apply(problemId_lookup_func, axis=1).dropna().astype(int)
        problemId = set(problemId_df)
    
    onehot_class = np.zeros((num_class, ))
    for pid in problemId:
        onehot_class[problem_class[pid]] += 1
        
    return np.insert(onehot_class, 0, user['rating'])
        

# Create data for prediction (changes problem_data)
def create_prediction_data(handle: str, problem_class: np.ndarray, problem_data: np.ndarray, up_stat, database = False):
    def increment_func(user_data, index):
        new_user_data = np.copy(user_data)
        if (index != 0):
            new_user_data[index] += 1
        return new_user_data
    
    # Creating user data
    user_data = create_user_data(handle, problem_class, database)
    index_arr = np.arange(user_data.shape[0]).reshape((-1, 1))
    user_data_table = np.apply_along_axis(lambda index: increment_func(user_data, index), axis = 1, arr = index_arr)
    user_data_width = user_data_table.shape[1]
    
    # stats data
    shape_arr = up_stat['length']
    mean_arr = up_stat['mean']
    std_arr = up_stat['std']
    cont_inp_width = shape_arr[0][1]
    
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
    
    # Concatenating user data and problem data
    indices1, indices2 = np.meshgrid(np.arange(user_data_table.shape[0]), np.arange(problem_data.shape[0]), indexing='ij')
    indices1, indices2 = indices1.flatten(), indices2.flatten()
    data = np.concatenate((user_data_table[indices1], problem_data[indices2]), axis=1)
    return data


# Calculates probabilistic advantage
def prob_advantage(handle, database = False):
    # Problem class data
    problem_class = np.load(address.data.problem_class)
    num_class = len(set(problem_class))
    
    # Problem data
    problem_data = np.load(address.data.imputed_prob)
    num_problem = problem_data.shape[0]
    
    # Loading stats data
    up_stat = np.load(address.data.user_problem_stat)
    
    # Prediction data
    data = create_prediction_data(handle, problem_class, problem_data, up_stat, database)
    
    # Probability data
    prob_data = predict(torch.Tensor(data)).to('cpu').detach().numpy()
    prob_data = prob_data[:, 0].reshape((-1, num_problem))
    base_probability = np.copy(prob_data[0])
    
    # del data
    del data
    
    # Weight for calculating weighted mean
    gamma = 0.9998      # Discount Factor for preferring new questions over older questions
    weights = np.geomspace(1, gamma**(num_problem-1), num_problem)
    weights /= np.sum(weights)
    
    # Calculating weighted mean of probability
    prob_data = np.matmul(prob_data, weights.reshape(-1, 1)).flatten()

    # Calculating advantage
    advantage = (prob_data - prob_data[0])[1:]
    
    # Calculating probabilistic advantage
    prob_adv = advantage[problem_class] * base_probability
    
    return base_probability, prob_adv


print(prob_advantage('ris04hit', database=True))