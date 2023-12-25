import sys
import os
import numpy as np
import pandas as pd
from pandarallel import pandarallel
import time
import shutil

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.data_process_utils import *               

pandarallel.initialize(verbose=1)

# Create user data
def user_problem_data():
    with open(address.log.user_problem, 'w') as sys.stdout:
        start_time = time.time()
        chunk_size = 4000
        df_user = pd.read_csv(address.data.handles).sample(frac=1, random_state=68)      # Random permutation
        
        chunk_ind = 0
        for chunk_offset in range(0, len(df_user), chunk_size):
            df_user_chunk = df_user[chunk_offset : chunk_offset+chunk_size].reset_index(drop = True)
            num_tag = len(pd.read_csv(address.data.tags))
            problem_class = np.load(address.data.problem_class)
            problem_data = np.load(address.data.imputed_prob)
            
            df_train_data = df_user_chunk.parallel_apply(lambda user: create_up_data(user, problem_class, problem_data, num_tag, start_time), axis=1)
            
            train_x_cont = np.concatenate(df_train_data['x_cont'])
            train_x_cat = np.concatenate(df_train_data['x_cat'])
            train_y = np.concatenate(df_train_data['y'])
            printf(f'Shape of data:\t\tx_cont: {train_x_cont.shape}\tx_cat: {train_x_cat.shape}\ty: {train_y.shape}')
            printf(f'Size of data (MB):\tx_cont: {train_x_cont.nbytes//(1<<20)}\tx_cat: {train_x_cat.nbytes//(1<<20)}\ty: {train_y.nbytes//(1<<20)}')
            printf(f'Datatype of data: \tx_cont: {train_x_cont.dtype}\tx_cat: {train_x_cat.dtype}\ty: {train_y.dtype}')

            np.savez_compressed(address.data.user_problem(chunk_ind), x_cont = train_x_cont, x_cat = train_x_cat, y = train_y)
            
            printf(f'\n{address.data.user_problem(chunk_ind)} created successfully\n')
            
            chunk_ind += 1
            
            del train_x_cont
            del train_x_cat
            del train_y
        printf(f'\n{address.data.user_problem_dir} created successfully')
    
    sys.stdout = sys.__stdout__
    printf(f'{address.data.user_problem_dir} created successfully')


# Main
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Required more command line arguments")
        sys.exit()
        
    if not os.path.exists(address.data.handles):
        printf(f'{address.data.handles} does not exist. Execute {address.src.scrape_raw} first.')
        sys.exit()
        
    if not os.path.exists(address.data.imputed_prob):
        printf(f'{address.data.imputed_prob} does not exist. Execute {address.src.impute_problem} first.')
        sys.exit()
        
    if not os.path.exists(address.data.problem_class):
        printf(f'{address.data.problem_class} does not exist. Execute {address.src.problem_classify} first.')
        sys.exit()
    
    if (sys.argv[1] != '1') and os.path.exists(address.data.user_problem_dir):
        printf(f'{address.data.user_problem_dir} already exists.')
        sys.exit()
    elif (sys.argv[1] == '1') and os.path.exists(address.data.user_problem_dir):
        shutil.rmtree(address.data.user_problem_dir)
        
    os.makedirs(address.data.user_problem_dir)
    user_problem_data()
        
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)