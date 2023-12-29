import pandas as pd
import numpy as np
import sys
import os
import asyncio
from sklearn.neighbors import KNeighborsRegressor

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.data_process_utils import *
from utils.model_utils import *
from utils.scrape_utils import *

# Insert New problems
def insert_problems():
    # Creating Model
    n_neighbor = 6
    data = np.load(address.data.imputed_prob)
    weights = create_weight(problem_Data = data)[1:]
    neigh = KNeighborsRegressor(n_neighbors=n_neighbor, metric=distance_func(weights), n_jobs=-1)
    neigh.fit(data[:, 1:], data[:, 0])
    
    # Getting problem data
    new_problem_data = asyncio.run(get_problem_data())
    old_problem_data = pd.read_csv(address.data.problems)
    
    print(new_problem_data, old_problem_data)


# Main
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Required more command line arguments")
        sys.exit()

    if (sys.argv[1] != '1'):
        printf(f'Need to set overwrite to 1 to insert new problems')
    else:
        if not os.path.exists(address.data.imputed_prob):
            printf(f'{address.data.imputed_prob} does not exist. Execute {address.src.impute_problem} first.')
            sys.exit()
        
        if not os.path.exists(address.data.problems):
            printf(f'{address.data.problems} does not exist. Execute {address.src.scrape_raw} first.')

        insert_problems()
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)