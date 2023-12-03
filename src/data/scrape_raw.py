import aiohttp
import asyncio
import time
import pandas as pd
import sys
import os
import ast

sys.path.append(os.path.abspath('src'))
from utils.scrape_utils import *
from utils.address_utils import *

# Creating handles.csv
async def user_data():
    async with aiohttp.ClientSession() as session:
        with open(address.log.scrape_raw, 'w') as sys.stdout:
            start_time = time.time()
            
            # Requesting list of users
            user_list_request = asyncio.create_task(request_json(session, api_url('ur')))
            user_list = await asyncio.gather(user_list_request)
            df = pd.DataFrame(user_list[0])
            drop_label = ['lastName',
                          'country',
                          'city',
                          'friendOfCount',
                          'titlePhoto',
                          'avatar',
                          'firstName',
                          'organization', 
                          'vkId',
                          'email',
                          'openId']
            df = df.drop(columns=drop_label)
            df.to_csv(address.data.handles, index = False)
            printf(f'{address.data.handles} created\t\t\tTime Taken: {time.time() - start_time}')
                        
        sys.stdout = sys.__stdout__
        printf(f'{address.data.handles} created')


# Creating problems.csv
async def problem_data():
    async with aiohttp.ClientSession() as session:
        with open(address.log.scrape_raw, 'a') as sys.stdout:
            start_time = time.time()
            
            # Requesting list of problems
            problem_list_request = asyncio.create_task(request_json(session, api_url('pp')))
            problem_list = await asyncio.gather(problem_list_request)
            
            # Combining problem and its statistics in single df
            df_problem = pd.DataFrame(problem_list[0]['problems'])
            df_statistics = pd.DataFrame(problem_list[0]['problemStatistics'])
            df = pd.concat((df_problem.drop(columns=['name']), df_statistics.drop(columns=['contestId', 'index'])), axis=1)
            df.to_csv(address.data.problems, index = False)
            printf(f'{address.data.problems} created\t\t\tTime Taken: {time.time()-start_time}')

        sys.stdout = sys.__stdout__
        printf(f'{address.data.problems} created')


# Creating tag.csv
async def tag_data():
    async with aiohttp.ClientSession() as session:
        with open(address.log.scrape_raw, 'a') as sys.stdout:
            # Creating a new df corresponding to tags
            start_time = time.time()
            tag_list = []      # Problem Id is the serial number of problem in problems.csv
            df = pd.read_csv(address.data.problems)
            df['tags'] = df['tags'].apply(ast.literal_eval)
            
            # Creating new tag dataframe
            for ind_problem, row_problem in df.iterrows():
                for tag in row_problem['tags']:
                    for ind_tag in range(len(tag_list)):
                        if tag_list[ind_tag]['tags'] == tag:
                            tag_list[ind_tag]['problemId'].append(ind_problem)
                            break
                    else:
                        tag_list.append({'tags': tag, 'problemId': [ind_problem]})
            df_tag = pd.DataFrame(tag_list)
            df_tag.to_csv(address.data.tags, index = False)
            printf(f'{address.data.tags} created\t\t\tTime Taken: {time.time()-start_time}')
        
        sys.stdout = sys.__stdout__
        printf(f'{address.data.tags} created')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Required more command line arguments")
        sys.exit()
    
    if (sys.argv[1] == '1') or (not os.path.exists(address.data.handles)):
        asyncio.run(user_data())
    else:
        print(f'{address.data.handles} already exists')
    
    if (sys.argv[1] == '1') or (not os.path.exists(address.data.problems)):
        asyncio.run(problem_data())
    else:
        print(f'{address.data.problems} already exists')
        
    if (sys.argv[1] == '1') or (not os.path.exists(address.data.tags)):
        asyncio.run(tag_data())
    else:
        print(f'{address.data.tags} already exists')