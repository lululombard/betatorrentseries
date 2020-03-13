import os
import requests
from dotenv import load_dotenv

def get_betaseries_token():
    data = {
        'login': os.environ['BETASERIES_LOGIN'],
        'password': os.environ['BETASERIES_MD5_PASSWORD'],
        'key': os.environ['BETASERIES_API_KEY']
    }

    response = requests.post('https://api.betaseries.com/members/auth', data=data)

    return response.json().get('token')


def get_betaseries_headers(token):
    return {
        'X-BetaSeries-Key': os.environ['BETASERIES_API_KEY'],
        'Authorization': 'Bearer {}'.format(token)
    }


def get_pending_series(token):
    response = requests.get('https://api.betaseries.com/shows/member', headers=get_betaseries_headers(token))

    print(response.json())

    return None

if __name__ == "__main__":
    load_dotenv()

    token = get_betaseries_token()

    shows = get_pending_series(token)
