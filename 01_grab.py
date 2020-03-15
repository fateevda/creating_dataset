#!.env/Scripts/python.exe

__doc__ = '''Скрипт скачивания исходных данных с сайта'''

import urllib
import requests
import requests_cache
import bs4

from pathlib import Path
from pprint import pprint
from tqdm import tqdm
import re

pattern = 'https://ria.ru/[\w|/]+.html'

root_url = r'https://ria.ru/sitemap_article.xml?date_start=20200301&date_end=20200315'


def load_robots(root: str) -> str:
    r = requests.get(urllib.parse.urljoin(root, 'robots.txt'))
    return r.content.decode('utf-8')


def main():   
    
    # Включаем кэшировие загруженных страниц
    raw_root = Path('corpus/raw')
    raw_root.mkdir(parents=True, exist_ok=True)
    requests_cache.install_cache(cache_name='corpus/raw_cache', backend='sqlite')

    # Посмотрим, что ждёт от нас сайт
    print('Содержимое robots.txt:', load_robots(root_url), sep='\n')

    # Получим список страниц для скачивания
    main_index = requests.get(urllib.parse.urljoin(root_url, ''))
    main_bs = bs4.BeautifulSoup(main_index.content.decode('utf-8'))
    main_links = re.findall(pattern, str(main_bs))
    # Сохраним страницы
    for i, link in tqdm(enumerate(main_links)):
        page_raw_text = requests.get(link).content
        print(link)
        with open((raw_root / str(i)).with_suffix('.html'), 'wb') as dst:
            dst.write(page_raw_text)



if __name__ == "__main__":
    main()