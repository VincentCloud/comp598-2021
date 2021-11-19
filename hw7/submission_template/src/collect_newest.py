import requests
import requests.auth
from pathlib import Path
import json
import argparse

CLIENT_ID = 'jb0x0qpJKVjA6ksd0fEQJA'
CLIENT_SECRET = 'Tllxf8cYnEGuo1KNsbH23G00smb7WA'

USER_NAME = 'fake_bot_hcz'
PASSWORD = 'password'
BASE_URL = 'https://oauth.reddit.com/r/'


def get_access_token(username, password):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {'grant_type': 'password', 'username': username, 'password': password}
    headers = {'User-Agent': 'Vincent'}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    return response.json()['access_token']


def get_posts_from_subreddit(subreddit, headers, limit=100):
    res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/new', headers=headers, params={'limit': limit})
    return res.json()['data']['children']


def get_post_and_save(subreddit, output_file):
    access_token = get_access_token(USER_NAME, PASSWORD)

    headers = {'User-Agent': 'Vincent', 'Authorization': f'bearer {access_token}'}
    post_info = get_posts_from_subreddit(subreddit, headers)

    # write the post_info into a json file
    with open(Path(f'{output_file}'), 'w+') as jf:
        jf.writelines([f'{json.dumps(post)}\n' for post in post_info])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide path to the output file and the name of the subreddit')

    parser.add_argument('-s', type=str, help='The name of the subreddit, it is either mcgill or concordia')
    parser.add_argument('-o', type=str, help='The path to the output file')

    args = parser.parse_args()

    if not args.s or not args.o:
        raise parser.error('No output file or subreddit name specified')

    # parse the argument into variables
    output_path = args.o
    subreddit_name = args.s

    get_post_and_save(subreddit_name, output_path)