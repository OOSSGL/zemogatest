import requests

api_key = 'KRy7l0v8wex3w8Sy5zThai3Ea'
access_token = '1220032047516921859-otvXjhExyUTZ5GLxssc9h5ORqtPZja'


def get_last_five_tweets(screen_name):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=5".format(screen_name)
    headers = {
        'authorization': 'OAuth oauth_consumer_key="{}" oauth_token="{}" oauth_version="1.0"'.format(api_key, access_token)
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    return response.json()
