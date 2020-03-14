import os
import requests
import re

class BetaSeries:
    token = None

    def __init__(self):
        data = {
            'login': os.environ['BETASERIES_LOGIN'],
            'password': os.environ['BETASERIES_MD5_PASSWORD'],
            'key': os.environ['BETASERIES_API_KEY']
        }

        response = requests.post('https://api.betaseries.com/members/auth', data=data)

        self.token = response.json().get('token')


    def get_betaseries_headers(self):
        return {
            'X-BetaSeries-Key': os.environ['BETASERIES_API_KEY'],
            'Authorization': 'Bearer {}'.format(self.token)
        }


    def mark_episode_downloaded(self, episode_id):
        data = {
            'id': episode_id
        }
        requests.post('https://api.betaseries.com/episodes/downloaded', data=data, headers=self.get_betaseries_headers())


    def mark_episode_not_downloaded(self, episode_id):
        data = {
            'id': episode_id
        }
        requests.delete('https://api.betaseries.com/episodes/downloaded', data=data, headers=self.get_betaseries_headers())


    def get_pending_series(self):
        response = requests.get('https://api.betaseries.com/episodes/list', headers=self.get_betaseries_headers())

        parsed_response = response.json()

        shows = []

        for show in parsed_response.get('shows', []):
            title = re.sub(r'\([^)]*\)', '', show.get('title', '')).strip()
            unseen = []
            for episode in show.get('unseen', []):
                if not episode.get('user', {}).get('downloaded'):
                    code = episode.get('code')
                    if code:
                        unseen.append({
                            'code': code,
                            'id': episode['id']
                        })

            if title and unseen:
                shows.append({
                    'name': title,
                    'to_download': unseen
                })

        return shows
