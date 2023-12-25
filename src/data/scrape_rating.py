import aiohttp
import asyncio
import time
import pandas as pd
import sys
import os
import threading

sys.path.append(os.path.abspath('src'))
from utils.scrape_utils import *
from utils.address_utils import *
from utils.data_process_utils import *

# Creating function for checking  corrupted files
def check_corrupt(batch_ind, batch_size, df_user):
    global file_checked
    global corrupt
    for ind, row in df_user.iterrows():
        if (ind-batch_ind)%batch_size == 0:
            try:
                lock = threading.Lock()
                with lock:
                    file_checked += 1
                temp_df = pd.read_csv(address.data.rating(row['handle']))
                if len(temp_df) == 0:
                    os.remove(address.data.rating(row['handle']))
                    lock = threading.Lock()
                    with lock:
                        printf(f"Removed {address.data.rating(row['handle'])} {ind}, Empty file")
                        corrupt = True
            except Exception as e:
                os.remove(address.data.rating(row['handle']))
                lock = threading.Lock()
                with lock:
                    printf(e)
                    printf(f"Removed {address.data.rating(row['handle'])} {ind}, Corrupted file")
                    corrupt = True


# termination condition
def terminate_execution(execution_num):
    global file_checked
    global corrupt
    
    # Re initialize variables
    start_time = time.time()
    file_checked = 0
    corrupt = False
    force_terminate = execution_num > 2
    
    # Checking if all files present
    df_user = pd.read_csv(address.data.handles)
    delete_ind = []
    for ind, row in df_user.iterrows():
        if (not os.path.exists(address.data.rating(row['handle']))):
            if force_terminate:
                delete_ind.append(ind)
            else:
                return False
    
    # Removing users whose data can not be extracted even in several tries
    if force_terminate:
        for ind in delete_ind:
            printf(f'deleting data for handle {df_user["handle"][ind]}')    # Not removing from submission for avoiding any later conflicts
        df_user = df_user.drop(delete_ind).reset_index(drop=True)
        df_user.to_csv(address.data.handles, index=False)
    
    # Checking for corrupted files
    batch_size = 10          # Number of Threads
    
    def print_status():
        while file_checked != len(df_user):
            time.sleep(30)
            printf(f'Files Checked: {file_checked}\t\tTime Taken: {time.time()-start_time}')
    
    print_thread = threading.Thread(target=print_status)
    print_thread.start()
    
    # Creating threads
    print("Checking Corrupted Files")
    thread_list = []
    for ind in range(batch_size):
        thread = threading.Thread(target=check_corrupt, args=(ind, batch_size, df_user))
        thread.start()
        thread_list.append(thread)
    
    # Waiting for threads to end
    for thread in thread_list:
        thread.join()
    print_thread.join()
        
    return not corrupt


# Creating rating directory
async def scrape_rating(overwrite = False):
    async with aiohttp.ClientSession() as session:
        if overwrite:
            mode = 'w'
        else:
            mode = 'a'
        with open(address.log.scrape_rating, mode) as sys.stdout:
            start_time = time.time()
            batch_size = 5          # Maximum number of parallel processes
            request_limit = 400     # Maximum number of request without sleep
            sleep_time = 20        # Sleep time to prevent overwhelming of server
            time_limit = 3          # time limit per batch
            delete_index = []
            
            # Reading required data
            df_user = pd.read_csv(address.data.handles)
            printf(f'\nRead required files\t\tTime taken: {time.time()-start_time}')
            
            # Creating required folder
            if (not os.path.exists(address.data.rating_dir)):
                os.mkdir(address.data.rating_dir)
            
            # Requesting rating for each user
            rating_list_request = []
            index_list = []
            num_request = 0
            for ind, row in df_user.iterrows():
                # Requesting list of rating changes
                new_insert = False
                if overwrite or (not os.path.exists(address.data.rating(row['handle']))):
                    rating_list_request.append(asyncio.create_task(request_json(session, api_url('ur', handle=row['handle']))))
                    index_list.append(ind)
                    num_request += 1
                    new_insert = True
                
                # Fetching ratings
                if (ind == len(df_user)-1) or (new_insert and (num_request%batch_size == 0)):
                    request_time = time.time() 
                    rating_list = await asyncio.gather(*rating_list_request)
                    for i in range(len(rating_list)):
                        # Modify ratings
                        user_handle = df_user['handle'][index_list[i]]
                        processed_ratings = []
                        if rating_list[i] is None:  # If error was encountered while retrieving ratings
                            continue
                        for curr_rating in rating_list[i]:
                            processed_ratings.append(curr_rating)
                        
                        # Saving ratings to csv files
                        processed_ratings_df = pd.DataFrame(processed_ratings)
                        if len(processed_ratings_df) != 0:
                            processed_ratings_df.to_csv(address.data.rating(user_handle), index=False)
                            update_submission_thread = threading.Thread(target=update_submission, 
                                                                        args=(user_handle, processed_ratings_df, overwrite))
                            update_submission_thread.start()
                        else:
                            delete_index.append(index_list[i])
                    printf(f'{ind+1}/{len(df_user)} users\' ratings fetched\tTime Taken: {time.time()-start_time}')
                    rating_list_request = []
                    index_list = []
                    
                    # Imposing rate limit
                    while time.time() - request_time < time_limit:
                        time.sleep(time_limit/10)
                        
                # Sleeping to prevent server overwhelming
                if new_insert and (num_request%request_limit == 0):
                    printf(f'Sleeping for {sleep_time} seconds to prevent overwhelming of server')
                    time.sleep(sleep_time)
            printf(f'{address.data.rating_dir} created\t\t\tTime Taken: {time.time() - start_time}\n')
            
            # Removing from handles.csv
            for ind in delete_index:
                printf(f'Removed {df_user["handle"][ind]} {ind} from handles.csv')
            df_user = df_user.drop(delete_index).reset_index(drop=True)
            df_user.to_csv(address.data.handles)
                    
        sys.stdout = sys.__stdout__
        printf(f'{address.data.rating_dir} completed')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        printf("Required more command line arguments")
        sys.exit()
        
    if (not os.path.exists(address.data.handles)):
        printf(f"{address.data.handles} not present.\nExecute {address.src.scrape_raw} first")
        sys.exit()
        
    file_checked = 0
    corrupt = False
    execution_num = 0
    while not terminate_execution(execution_num):
        if execution_num != 0:
            printf('\nRestarting execution\n')
            time.sleep(20)
        execution_num += 1
        try:
            asyncio.run(scrape_rating(sys.argv[1] == '1'))
        except Exception as e:
            sys.stdout = sys.__stdout__
            printf(e)
            execution_num = 0
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)