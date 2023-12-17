import pandas as pd
import ast
import numpy as np
import os
import sys
import sklearn.impute as sk_imp

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.data_process_utils import *


# Convert data into numpy array
def problem_df_to_np(df_problem: pd.DataFrame):
    df_tag = pd.read_csv(address.data.tags)
    df_tag['problemId'] = df_tag['problemId'].apply(ast.literal_eval)
    num_tag = len(df_tag)
    processed_data = []
    
    # Creating numpy array of data
    for ind_prob, problem in df_problem.iterrows():
        converted_problem = [problem['difficulty'], problem['points'], problem['rating'], problem['solvedCount']]
        converted_problem.extend([0]*num_tag)
        processed_data.append(converted_problem)

    # One Hot encoding for tags
    for ind_tag, row_tag in df_tag.iterrows():
        for problemId in row_tag['problemId']:
            processed_data[problemId][4 + ind_tag] = 1
        
    processed_data = np.array(processed_data)
    
    return num_tag, processed_data


# Impute problem
def impute_knn(data, weights):
    imp_knn = sk_imp.KNNImputer(missing_values=np.nan, n_neighbors=2, metric = distance_func(weights))
    imputed_data = imp_knn.fit_transform(data)
    np.save(address.data.imputed_prob, imputed_data)


# Main
if __name__ == '__main__':
    # Checking data requirements
    if not os.path.exists(address.data.problems):
        printf(f'{address.data.problems} does not exist')
        sys.exit()
    
    # Checking overwrite
    if (sys.argv[1] != '1') and os.path.exists(address.data.imputed_prob):
        printf(f'{address.data.imputed_prob} already exists')
        sys.exit()
    
    df_problem = pd.concat((pd.read_csv(address.data.problems), pd.read_csv(address.data.problem_diff)), axis=1)
    num_tag, processed_prob = problem_df_to_np(df_problem)
    impute_knn(processed_prob, create_weight(num_tag))
    printf(f'Created {address.data.imputed_prob} Successfully')
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)