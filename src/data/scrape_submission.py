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
                temp_df = pd.read_csv(address.data.submission(row['handle']))
                if len(temp_df) == 0:
                    os.remove(address.data.submission(row['handle']))
                    lock = threading.Lock()
                    with lock:
                        printf(f"Removed {address.data.submission(row['handle'])} {ind}, Empty file")
                        corrupt = True
            except Exception as e:
                os.remove(address.data.submission(row['handle']))
                lock = threading.Lock()
                with lock:
                    printf(e)
                    printf(f"Removed {address.data.submission(row['handle'])} {ind}, Corrupted file")
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
        if (not os.path.exists(address.data.submission(row['handle']))):
            if force_terminate:
                delete_ind.append(ind)
            else:
                return False
    
    # Removing users whose data can not be extracted even in several tries
    if force_terminate:
        for ind in delete_ind:
            printf(f'deleting data for handle {df_user["handle"][ind]}')
        df_user = df_user.drop(delete_ind).reset_index(drop=True)
        df_user.to_csv(address.data.handles, index=False)        

    # Checking for corrupted files
    batch_size = 10          # Number of Threads
    
    def print_status():
        while file_checked != len(df_user):
            time.sleep(30)
            print(f'Files Checked: {file_checked}\t\tTime Taken: {time.time()-start_time}')
    
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


# Creating submission directory
async def scrape_submission(overwrite = False):
    async with aiohttp.ClientSession() as session:
        if overwrite:
            mode = 'w'
        else:
            mode = 'a'
        with open(address.log.scrape_submission, mode) as sys.stdout:
            start_time = time.time()
            batch_size = 5          # Maximum number of parallel processes
            request_limit = 400     # Maximum number of request without sleep
            sleep_time = 20        # Sleep time to prevent overwhelming of server
            time_limit = 3          # time limit per batch
            delete_index = []
            
            # Reading required data
            df_user = pd.read_csv(address.data.handles)
            df_problem = pd.read_csv(address.data.problems)
            problemId_func = problemId_lookup(df_problem)
            printf(f'\nRead required files\t\tTime taken: {time.time()-start_time}')
            
            # Creating required folder
            if (not os.path.exists(address.data.submission_dir)):
                os.mkdir(address.data.submission_dir)
            
            # Requesting submission for each user
            submission_list_request = []
            index_list = []
            num_request = 0
            for ind, row in df_user.iterrows():
                # Requesting list of submissions
                new_insert = False
                if overwrite or (not os.path.exists(address.data.submission(row['handle']))):
                    submission_list_request.append(asyncio.create_task(request_json(session, api_url('us', handle=row['handle']))))
                    index_list.append(ind)
                    num_request += 1
                    new_insert = True
                
                # Fetching submissions
                if (ind == len(df_user)-1) or (new_insert and (num_request%batch_size == 0)):
                    request_time = time.time() 
                    submission_list = await asyncio.gather(*submission_list_request)
                    for i in range(len(submission_list)):
                        # Modify Submissions
                        user_handle = df_user['handle'][index_list[i]]
                        processed_submissions = []
                        if submission_list[i] is None:  # If error was encountered while retrieving submissions
                            continue
                        for curr_submission in submission_list[i]:
                            if len(curr_submission['author']['members']) != 1:      # Ignoring submissions of parties with more than one members
                                continue
                            curr_submission['problemId'] = problemId_func(curr_submission['problem'])   # Inserting problemId to submission
                            if curr_submission['problemId'] is None:
                                continue
                            del curr_submission['problem']
                            curr_submission['handle'] = user_handle             # Inserting handle of user to submission
                            curr_submission['participantType'] = curr_submission['author']['participantType']   # Inserting participant Type
                            curr_submission['startTimeSeconds'] = curr_submission['author']['startTimeSeconds'] # Inserting start time of author
                            del curr_submission['author']
                            processed_submissions.append(curr_submission)
                        
                        # Saving submission to csv files
                        processed_submissions_df = pd.DataFrame(processed_submissions)
                        if len(processed_submissions_df) != 0:
                            processed_submissions_df.to_csv(address.data.submission(user_handle), index=False)
                        else:
                            delete_index.append(index_list[i])
                    printf(f'{ind+1}/{len(df_user)} users\' submissions fetched\tTime Taken: {time.time()-start_time}')
                    submission_list_request = []
                    index_list = []
                    
                    # Imposing rate limit
                    while time.time() - request_time < time_limit:
                        time.sleep(time_limit/10)
                        
                # Sleeping to prevent server overwhelming
                if new_insert and (num_request%request_limit == 0):
                    printf(f'Sleeping for {sleep_time} seconds to prevent overwhelming of server')
                    time.sleep(sleep_time)
            printf(f'{address.data.submission_dir} created\t\t\tTime Taken: {time.time() - start_time}\n')
            
            # Removing from handles.csv
            for ind in delete_index:
                printf(f'Removed {df_user["handle"][ind]} {ind} from handles.csv')
            df_user = df_user.drop(delete_index).reset_index(drop=True)
            df_user.to_csv(address.data.handles)
                    
        sys.stdout = sys.__stdout__
        printf(f'{address.data.submission_dir} completed')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        printf("Required more command line arguments")
        sys.exit()
        
    if (not os.path.exists(address.data.handles)):
        printf(f"{address.data.handles} not present.\nExecute {address.src.scrape_raw} first")
        sys.exit()

    if (not os.path.exists(address.data.problems)):
        printf(f"{address.data.problems} not present.\nExecute {address.src.scrape_raw} first")
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
            asyncio.run(scrape_submission(sys.argv[1] == '1'))
        except Exception as e:
            sys.stdout = sys.__stdout__
            printf(e)
            execution_num = 0
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)