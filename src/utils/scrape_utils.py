import sys
import json

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
    if methodName == 'ur':
        return f'{url}/user.ratedList'
    
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

