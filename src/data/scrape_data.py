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
    # args:: contestId, showUnofficial
    if methodName == 'cs':
        return f'{url}/contest.standings?contestId={contestID}&showUnofficial={showUnofficial}'
    
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
            batch_size = 6
            request_limit = 140
            sleep_time = 140
            
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
                    standings = await asyncio.gather(*standings_request)
                    standings_request = []
                    for stand in standings:
                        if stand is not None:
                            for rank_list_row in stand['rows']:
                                for member in rank_list_row['party']['members']:
                                    users.add(member['handle'])
                    printf(f'{loop_ind}/{len(contest_list[0])} Contests Fetched\tTime Taken: {time.time() - start_time}\tNum_users:{len(users)}')
                if (loop_ind % request_limit == 0):
                    printf("Sleeping for avoiding server overwhelming")
                    time.sleep(sleep_time)
            df = pd.DataFrame({'handle': sorted(list(users))})
            df.to_csv('data/raw/scrapped_data/handles.csv', index = False)
        print('handles.csv created')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        printf("Requires more command line arguments")
        sys.exit()
    
    if sys.argv[1] == 'user':       # Generate user.csv
        asyncio.run(user_data())