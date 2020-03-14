from clutch.core import Client
import os
import shutil
import math
import time

extensions = ['webm', 'mkv', 'ts', 'avi', 'mts', 'm2ts', 'mov', 'wmv', 'mp4', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'divx']

def get_transmission_client():
    address = os.environ.get('TRANSMISSION_URL')
    username = os.environ.get('TRANSMISSION_USER')
    password = os.environ.get('TRANSMISSION_PASSWORD')
    return Client(address=address, username=username, password=password)

def download_torrent(link, show_name, episode_code):
    transmission = get_transmission_client()

    download_dir = os.environ.get('TRANSMISSION_DIRECTORY')
    final_directory = os.environ.get('FINAL_DIRECTORY')

    response = transmission.torrent.add(filename=link, download_dir=download_dir)
    torrent_id = response['id']
    try:
        file_name = None
        file_extension = None
        file_size = 0

        timeout = 0
        while timeout < 300:
            timeout += 1
            time.sleep(1)
            files = transmission.torrent.files(ids=[torrent_id])[torrent_id].get('files')
            for file in files:
                for extension in extensions:
                    if file['name'].lower().endswith('.' + extension) and file['length'] > file_size:
                        file_name = file['name']
                        file_extension = extension
                        file_size = file['length']
            if file_name:
                break

        if not file_name:
            raise ValueError('No compatible format has been found')

        progress = 0
        while progress < 100:
            time.sleep(1)
            progress = math.floor(transmission.torrent.percent_done(ids=[torrent_id])[torrent_id] * 100)

        series_folder = '{}/{}'.format(final_directory, show_name)

        if not os.path.exists(series_folder):
            os.makedirs(series_folder)

        final_file = '{}/{} {}.{}'.format(series_folder, show_name, episode_code, file_extension)

        shutil.copyfile('{}/{}'.format(download_dir, file_name), final_file)

        transmission.torrent.remove(ids=[torrent_id], delete_local_data=True)

        return final_file
    except Exception as e:
        try:
            transmission.torrent.remove(ids=[torrent_id], delete_local_data=True)
        except Exception:
            pass
        raise e

    return None
