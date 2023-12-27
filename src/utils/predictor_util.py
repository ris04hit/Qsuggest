import sys
import os
import numpy as np
import pandas as pd
import time
import multiprocessing

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from models.up_probability_model import predict
from utils.data_process_utils import create_user_data

home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
prefix = os.path.relpath(home_directory)
address = Address(prefix = prefix)

# Calculating probability for all problems
def problem_prob(handle, plus_class = []):
    predict_func = predict()
    
    # Loading data
    problem_class = np.load(address.data.problem_class)
    num_problems = len(pd.read_csv(address.data.problems))
    probability = []
    
    # Creating user data
    user_data = create_user_data(handle, problem_class)
    
    # Predicting probability
    for problemId in range(num_problems):
        probability.append(predict_func(problemId, plus_class=plus_class, user_data=user_data)[0])
        
    return np.array(probability)


# Function to enable multiprocessing in prob_advantage
def multiprocessing_func(data):
    handle = data[0]
    class_ind = data[1]
    weights = data[2]
    return np.matmul(weights, problem_prob(handle, plus_class=[class_ind])[:, 0])

# Predicting best problem
def prob_advantage(handle):
    # Probability for user without modification
    probability = problem_prob(handle)[:, 0]
    
    # Weight for calculating weighted mean
    gamma = 0.9998      # Discount Factor for preferring new questions over older questions
    weights = np.geomspace(1, gamma**(probability.shape[0]-1), probability.shape[0])
    weights /= sum(weights)
    weights = weights
    
    # Problem class data
    problem_class = np.load(address.data.problem_class)
    num_class = len(set(problem_class))
    
    # Function for probability after modification
    with multiprocessing.Pool() as pool:
        mean_prob = pool.map(multiprocessing_func, [(handle, class_ind, weights) for class_ind in range(num_class)])
    
    # Calculating probabilistic advantage for each question
    base_prob = np.matmul(weights, probability)
    mean_prob -= base_prob
    advantage = np.copy(probability)
    for problemId in range(probability.shape[0]):
        advantage[problemId] *= mean_prob[problem_class[problemId]]
        
    return probability, advantage
