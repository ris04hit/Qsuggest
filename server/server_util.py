import sys
import os
import pandas as pd

sys.path.append(os.path.abspath('src'))
from utils.predictor_util import prob_advantage
from utils.address_utils import *

def create_output_data(inp_data):
    # Getting from input data
    handle = inp_data['handle']
    
    # Getting predictions
    base_prob, prob_adv, solved_problem = prob_advantage(handle)
    
    # Getting problem data
    df_problem = pd.read_csv(address.data.problems)[['contestId', 'index']]
    
    return {
        'base_probability': base_prob.tolist(),
        'probability_advantage': prob_adv.tolist(),
        'solved_problem': list(solved_problem),
        'problem_data': df_problem.to_dict()
    }