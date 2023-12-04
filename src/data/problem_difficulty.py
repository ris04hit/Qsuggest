import time
import pandas as pd
import sys
import os
import threading
import warnings
import numpy as np
import sklearn.linear_model as sk
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('src'))
from utils.scrape_utils import *
from utils.address_utils import *


# For printing log while working in multiple threads
def print_status():
    while user_processed != len(df_user):
        printf(f'{user_processed}/{len(df_user)} Users processed\t\tTime taken:{time.time() - start_time}')
        time.sleep(30)


# For finding problem difficulty individually for user
def process_user(thread_ind):
    global user_processed
    global num_wrong
    global num_rating
    for ind_user, row_user in df_user.iterrows():
        if ind_user%num_thread != thread_ind:       # Parallel distribution of work
            continue
        
        # Initializing variables
        ind_rating = row_user['maxRating']//rating_size        # index for rating class of the user
        df_submission = pd.read_csv(address.data.submission(row_user['handle']))
        num_wrong_user = np.zeros((len(df_problem,)))      # Number of wrong submissions before correct submission + 1 {if correct submission}
        correct_submitted_user = np.zeros((len(df_problem,)))      # 1 if there is correct submission for problem by user else 0
        
        # Checking of problems attempted by the user
        for problemId in set(df_submission['problemId']):
            lock = threading.Lock()
            with lock:
                num_rating[ind_rating, problemId] += 1
        
        # Calculating number of wrong answers before correct answer
        for ind_sub, row_sub in df_submission.iterrows():
            problemId = row_sub['problemId']
            if correct_submitted_user[problemId]:
                continue
            verdict = row_sub['verdict']
            num_wrong_user[problemId] += 1
            if verdict == 'OK':
                correct_submitted_user[problemId] = 1
        
        # Calcualing difficulty
        num_ease_user = 1/num_wrong_user        # Calculating 1 - difficulty = easiness
        num_ease_user[np.isinf(num_ease_user)] = 0      # Changing infinities to one for ensuring there zero contribution
        num_ease_user *= correct_submitted_user     # To ensure that problems with no correct submission has zero easiness

        # Updating difficulty globally
        lock = threading.Lock()
        with lock:
            num_wrong[ind_rating] += num_ease_user
            user_processed += 1
        

# Function for calculating weighted average difficulty
def calculate_score(individual_score: np.ndarray, weights: np.ndarray):
    printf(f'Calculating Final difficulties:')
    
    weight2d = weights.reshape((-1, 1))
    difficulty_problem = []
    
    for ind_problem in range(individual_score.shape[1]):
        score = individual_score[:, ind_problem]
        non_nan_indices = np.where(~np.isnan(score))
        if non_nan_indices[0].shape[0] == 0:        # Problem never attempted
            difficulty_problem.append(np.nan)
            printf(f"Problem {ind_problem}, not attempted, needs to be predicted")
            continue
        
        # Training linear regression model
        model = sk.LinearRegression()
        model.fit(weight2d[non_nan_indices], score[non_nan_indices])
        predicted_score = model.predict(weight2d)
        predicted_score[non_nan_indices] = score[non_nan_indices]
        predicted_score[predicted_score < 0] = 0
        predicted_score[predicted_score > 1] = 1

        # Calculating weighted easiness
        difficulty = 1 - np.matmul(weights, predicted_score)
        difficulty_problem.append(difficulty)
    
    return np.array(difficulty_problem)


# Main
if __name__ == '__main__':
    if (sys.argv[1] != '1') and os.path.exists(address.data.problem_diff):
        printf(f'{address.data.problem_diff} already exists')
        sys.exit()

    with open(address.log.problem_diff , 'w') as sys.stdout:
        warnings.filterwarnings("ignore")
        
        start_time = time.time()
        
        # Load Data
        df_user = pd.read_csv(address.data.handles)
        df_problem = pd.read_csv(address.data.problems)
        
        # Initialize variables
        rating_size = 40            # width of rating
        delta_rating = max(df_user['maxRating'])//rating_size + 1       # number of classes in which user is divide on basis of rating
        weights = np.array([rating_size*(ind + 1/2) for ind in range(delta_rating)])        # Weights for user as per rating
        weights/=np.sum(weights)
        num_wrong = np.zeros((delta_rating, len(df_problem)))       # Total Easiness
        num_rating = np.zeros((delta_rating, len(df_problem)))     # Stores number of users with given rating for particular problem
        user_processed = 0
        num_thread = 10
        
        # Thread for printing log
        print_thread = threading.Thread(target=print_status)
        print_thread.start()

        # Thread for calculating individual score
        user_thread = [threading.Thread(target=process_user, args = (thread_ind,)) for thread_ind in range(num_thread)]
        for thread in user_thread:
            thread.start()
        for thread in user_thread:
            thread.join()

        # Closing print thread
        print_thread.join()

        # Calculating final difficulties
        individual_score = num_wrong/num_rating         # Score of easiness
        difficulty_problem = calculate_score(individual_score, weights)

        pd.DataFrame({'difficulty': difficulty_problem}).to_csv(address.data.problem_diff, index=False)

        printf(f"{address.data.problem_diff} created\t\tTime Taken: {time.time() - start_time}")

        warnings.resetwarnings()
    
    sys.stdout = sys.__stdout__
    printf(f"{address.data.problem_diff} created")