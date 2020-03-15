import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_magnet_link(page_url):
    response = requests.get(page_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        if href.startswith('magnet:'):
            return href

    return None


def get_best_link(show, episode):
    url = 'https://1337x.to/sort-search/{}%20{}/size/desc/1/'.format(show, episode)

    tries = 0

    while tries < 10:
        response = requests.get(url, headers={'User-Agent': UserAgent().chrome})

        if not response.text:
            tries += 1
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            links = soup.find('tbody').find('tr').find_all('a')
            for link in links:
                href = link.get('href')
                if href and href.startswith('/torrent'):
                    return get_magnet_link('https://1337x.to' + href)

        except AttributeError:
            break

    return None
