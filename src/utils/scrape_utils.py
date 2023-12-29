import sys
import json
import pandas as pd
import aiohttp
import asyncio

# Flushing output after printing
def printf(*args):
    print(*args)
    sys.stdout.flush()


# Creating url for api request
def api_url(methodName, contestID = None, gym = False, handle = None, handles = [], showUnofficial = True):
    url = 'https://codeforces.com/api'
    # contest list
    # args: gym
    if methodName == 'cl':    
        return f'{url}/contest.list?gym={gym}'
    
    # contest standing
    # args: contestId, showUnofficial
    if methodName == 'cs':
        return f'{url}/contest.standings?contestId={contestID}&showUnofficial={showUnofficial}'
    
    # problemset problems
    # args: None
    if methodName == 'pp':
        return f'{url}/problemset.problems'
    
    # user rated List
    # args: None
    if methodName == 'url':
        return f'{url}/user.ratedList'
    
    # user ratings
    # args: handle
    if methodName == 'ur':
        return f'{url}/user.rating?handle={handle}'
    
    # user status
    # args: handle
    if methodName == 'us':
        return f'{url}/user.status?handle={handle}'
    
    # user info
    # args: handle
    if methodName == 'ui':
        return f'{url}/user.info?handles={";".join(handles)}'
    
    return None


# Requesting data in json format
async def request_json(session, url):
    async with session.get(url) as response:
        try:
            data = await response.text()
            data = json.loads(data)
            if data['status'] == 'OK':
                return data['result']
            else:
                printf(f"Codeforces API Error: {data['comment']}")
                return None
        except Exception as ex:
            printf(f"JSON Error: {ex}")
            return None


# Lookup for problemId
def problemId_lookup(df_problem: pd.DataFrame):
    problem_dict = {}
    for problemId, row in df_problem.iterrows():
        problem_dict[(row['contestId'], row['index'])] = problemId
    def return_func(problem):
        # print(problem)
        if ('contestId' in problem) and ('index' in problem):
            key = (problem['contestId'], problem['index'])
            if key in problem_dict:
                return problem_dict[key]
            return None
        return None
    return return_func


# Get user info
async def get_user_info(handle):
    async with aiohttp.ClientSession() as session:
        user_info_request = asyncio.create_task(request_json(session, api_url('ui', handles=[handle])))
        user_info = await asyncio.gather(user_info_request)
        return user_info[0][0]
    
# Get user submission
async def get_user_submission(handle):
    async with aiohttp.ClientSession() as session:
        user_submission_request = asyncio.create_task(request_json(session, api_url('us', handle=handle)))
        user_submission = await asyncio.gather(user_submission_request)
        return user_submission[0]