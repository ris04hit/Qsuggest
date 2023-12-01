import aiohttp
import asyncio
import time
import pandas as pd
import sys
import os
import ast

sys.path.append(os.path.abspath('src'))
from utils.scrape_utils import *

# Creating handles.csv
async def user_data():
    async with aiohttp.ClientSession() as session:
        with open('logs/scrape_raw.log', 'w') as sys.stdout:
            start_time = time.time()
            
            # Requesting list of users
            user_list_request = asyncio.create_task(request_json(session, api_url('ur')))
            user_list = await asyncio.gather(user_list_request)
            df = pd.DataFrame(user_list[0])
            df.to_csv('data/scraped/handles.csv', index = False)
            printf(f'handles.csv created\t\t\tTime Taken: {time.time() - start_time}')
                        
        sys.stdout = sys.__stdout__
        printf('handles.csv created')

# Creating problems.csv
async def problem_data():
    async with aiohttp.ClientSession() as session:
        with open('logs/scrape_raw.log', 'a') as sys.stdout:
            start_time = time.time()
            
            # Requesting list of problems
            problem_list_request = asyncio.create_task(request_json(session, api_url('pp')))
            problem_list = await asyncio.gather(problem_list_request)
            
            # Combining problem and its statistics in single df
            df_problem = pd.DataFrame(problem_list[0]['problems'])
            df_statistics = pd.DataFrame(problem_list[0]['problemStatistics'])
            df = pd.concat((df_problem, df_statistics.drop(columns=['contestId', 'index'])), axis=1)
            df.to_csv('data/scraped/problems.csv', index = False)
            printf(f'problems.csv created\t\tTime Taken: {time.time()-start_time}')

        sys.stdout = sys.__stdout__
        printf('problems.csv created')

# Creating tag.csv
async def tag_data():
    async with aiohttp.ClientSession() as session:
        with open('logs/scrape_raw.log', 'a') as sys.stdout:
            # Creating a new df corresponding to tags
            start_time = time.time()
            tag_list = []      # Problem Id is the serial number of problem in problems.csv
            df = pd.read_csv('data/scraped/problems.csv')
            df['tags'] = df['tags'].apply(ast.literal_eval)
            
            # Creating new tag dataframe
            for ind_problem, row_problem in df.iterrows():
                for tag in row_problem['tags']:
                    for ind_tag in range(len(tag_list)):
                        if tag_list[ind_tag]['tags'] == tag:
                            tag_list[ind_tag]['ProblemId'].append(ind_problem)
                            break
                    else:
                        tag_list.append({'tags': tag, 'ProblemId': [ind_problem]})
            df_tag = pd.DataFrame(tag_list)
            df_tag.to_csv('data/scraped/tags.csv', index = False)
            printf(f'tag.csv created\t\t\t\tTime Taken: {time.time()-start_time}')
        
        sys.stdout = sys.__stdout__
        printf('tag.csv created')


if __name__ == '__main__':
    asyncio.run(user_data())
    asyncio.run(problem_data())
    asyncio.run(tag_data())