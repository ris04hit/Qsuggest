import sys
import os
import pandas as pd

sys.path.append(os.path.abspath('src'))
from utils.predictor_util import prob_advantage, prob_single
from utils.address_utils import *

def create_output_data(inp_data):
    # Getting from input data
    handle = inp_data['handle']
    user_info = inp_data['user_info'] if 'user_info' in inp_data else None
    submission = inp_data['submission'] if 'submission' in inp_data else None
    
    # Taking Care None handle
    if handle is None:
        return {}
    
    # Getting predictions
    base_prob, prob_adv, solved_problem = prob_advantage(handle, user_info=user_info, submission=submission)
    
    # Getting problem data
    df_problem = pd.read_csv(address.data.problems)[['contestId', 'index']]
    
    return {
        'base_probability': base_prob.tolist(),
        'probability_advantage': prob_adv.tolist(),
        'solved_problem': list(solved_problem),
        'problem_data': df_problem.to_dict()
    }
    
def predict_probability(inp_data):
    # Getting from input data
    handle = inp_data['handle']
    problem = inp_data['problem']
    
    return prob_single(handle, problem)