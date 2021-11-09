import requests
import requests.auth

if __name__ == '__main__':
    client_auth = requests.auth.HTTPBasicAuth('jb0x0qpJKVjA6ksd0fEQJA', 'Tllxf8cYnEGuo1KNsbH23G00smb7WA')
    post_data = {'grant_type': 'password', 'username': 'fake_bot_hcz', 'password': 'password'}
    headers = {'User-Agent': 'Vincent'}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    print(response.json())

