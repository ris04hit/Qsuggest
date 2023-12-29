import pandas as pd
import numpy as np
import os
import sys
from sklearn.impute import KNNImputer
import ast

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.data_process_utils import *


# Impute problem
def impute_knn(data, weights, num_neighbors):
    imp_knn = KNNImputer(missing_values=np.nan, n_neighbors = num_neighbors, metric = distance_func(weights))
    imputed_data = imp_knn.fit_transform(data)
    np.save(address.data.imputed_prob, imputed_data)


# Main
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Required more command line arguments")
        sys.exit()
    
    # Checking overwrite
    if (sys.argv[1] != '1') and os.path.exists(address.data.imputed_prob):
        printf(f'{address.data.imputed_prob} already exists')
        sys.exit()
        
    # Checking data requirements
    if not os.path.exists(address.data.problems):
        printf(f'{address.data.problems} does not exist. Execute {address.src.scrape_raw} first.')
        sys.exit()
    
    df_problem = pd.concat((pd.read_csv(address.data.problems), pd.read_csv(address.data.problem_diff)), axis=1)
    df_problem['tags'] = df_problem['tags'].apply(ast.literal_eval)
    num_tag, processed_prob = problem_df_to_np(df_problem)
    num_neighbors = 6
    impute_knn(processed_prob, create_weight(num_tag = num_tag, problem_Data = processed_prob), num_neighbors)
    printf(f'Created {address.data.imputed_prob} Successfully')
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)