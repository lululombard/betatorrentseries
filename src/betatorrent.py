import os
import traceback
from multiprocessing import Pool

from dotenv import load_dotenv

from helpers.betaseries import BetaSeries
from helpers.to1337x import get_best_link
from helpers.transmission import download_torrent

def download_show(metadata):
    show = metadata['show']
    episode = metadata['episode']
    link = get_best_link(show['name'], episode['code'])
    print('Link for {} {}: {}'.format(show['name'], episode['code'], link if link else 'not found'))
    if link:
        try:
            betaseries.mark_episode_downloaded(episode['id'])
            final_file = download_torrent(link, show['name'], episode['code'])
            print('Downloaded {} {} to {}'.format(show['name'], episode['code'], final_file))
        except Exception as e:
            traceback.print_exc()
            betaseries.mark_episode_not_downloaded(episode['id'])

if __name__ == "__main__":
    load_dotenv()

    betaseries = BetaSeries()

    shows = betaseries.get_pending_series()

    shows_to_download = []

    for show in shows:
        for episode in show['to_download']:
            shows_to_download.append({
                'show': show,
                'episode': episode
            })

    with Pool() as pool:
        pool.map(download_show, shows_to_download)
