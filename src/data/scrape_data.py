import aiohttp
import asyncio
import json
import time
import pandas as pd
import sys

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
    
    # user rating          
    # args: handle
    if methodName == 'ur':
        return f'{url}/user.rating?handle={handle}'
    
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


# Creating handles.csv
async def user_data():
    async with aiohttp.ClientSession() as session:
        with open('logs/scrape_user.txt', 'w') as sys.stdout:
            start_time = time.time()
            batch_size = 6              # Number of parallel requests
            request_limit = 140         # Number of request after which program sleeps temporarily
            sleep_time = 140            # Sleep time for preventing server overwhelming
            
            # Requesting Contests
            contest_list_request = asyncio.create_task(request_json(session, api_url('cl')))
            contest_list = await asyncio.gather(contest_list_request)
            printf(f"Contest List Fetched\t\tTime Taken: {time.time() - start_time}")
            
            standings_request, users = [], set()
            loop_ind = 0
            for contest in contest_list[0]:
                loop_ind += 1
                if contest['startTimeSeconds'] + contest['durationSeconds'] < time.time():       # Ensuring the contest has ended
                    standings_request.append(asyncio.create_task(request_json(session, api_url('cs', contestID = contest['id']))))
                if (batch_size == len(standings_request)) or (loop_ind == len(contest_list[0])):
                    # Fetching data for standings of contest
                    standings = await asyncio.gather(*standings_request)
                    standings_request = []
                    for stand in standings:
                        if stand is not None:       # If there was no error in fetching Data
                            for rank_list_row in stand['rows']:
                                for member in rank_list_row['party']['members']:
                                    users.add(member['handle'])
                    printf(f'{loop_ind}/{len(contest_list[0])} Contests Fetched\tTime Taken: {time.time() - start_time}\tNum_users:{len(users)}')
                if (loop_ind % request_limit == 0):
                    printf("Sleeping for avoiding server overwhelming")
                    time.sleep(sleep_time)
            df = pd.DataFrame({'handle': sorted(list(users))})
            df.to_csv('data/raw/scraped/handles.csv', index = False)
            printf(f'handles.csv created\tTime Taken: {time.time() - start_time}')
            
        sys.stdout = sys.__stdout__
        printf('handles.csv created')


# Creating problems.csv and tags.csv
async def problem_data():
    async with aiohttp.ClientSession() as session:
        with open('logs/scrape_problem.txt', 'w') as sys.stdout:
            start_time = time.time()
            
            # Requesting list of problems
            problem_list_request = asyncio.create_task(request_json(session, api_url('pp')))
            problem_list = await asyncio.gather(problem_list_request)
            printf(f"Problem List Fetched\t\tTime Taken: {time.time() - start_time}")
            
            # Combining problem and its statistics in single df
            df_problem = pd.DataFrame(problem_list[0]['problems'])
            df_statistics = pd.DataFrame(problem_list[0]['problemStatistics'])
            df = pd.concat((df_problem.drop(columns=['points']), df_statistics.drop(columns=['contestId', 'index'])), axis=1)
            df.to_csv('data/scraped/problems.csv', index = False)
            printf(f'problems.csv created\t\tTime Taken: {time.time()-start_time}')

        sys.stdout = sys.__stdout__
        printf('problems.csv created')
        
        with open('logs/scrape_problem.txt', 'a') as sys.stdout:
            # Creating a new df corresponding to tags
            tag_list = []      # Problem Id is the serial number of problem in problems.csv
            
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
    if len(sys.argv) <= 1:
        printf("Requires more command line arguments")
        sys.exit()
    
    if sys.argv[1] == 'user':       # Generate handles.csv
        asyncio.run(user_data())
    
    if sys.argv[1] == 'problem':    # Generate problems.csv and tags.csv
        asyncio.run(problem_data())