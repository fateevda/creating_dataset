#!.env/Scripts/python.exe

__doc__ = '''Скрипт скачивания исходных данных с сайта'''

import urllib
import requests
import requests_cache
import bs4

from pathlib import Path
from pprint import pprint
from tqdm import tqdm

root_url = r'https://ria.ru/'
topics = ['politics', 'world', 'economy', 'society','incidents', 
          'defense_safety', 'science', 'culture', 'religion', 'tourism']
# возникает вопрос, как работать со спортом

def load_robots(root: str) -> str:
    r = requests.get(urllib.parse.urljoin(root, 'robots.txt'))
    return r.content.decode('utf-8')


def main():
    
    # нужно сделать цикл по всем жанрам и подумать над тем, как увеличить 
    # количиство текстов и как не собирать лишние
    
    # for topic in topics:
    
    
    # Включаем кэшировие загруженных страниц
    raw_root = Path('corpus/raw/politics')
    raw_root.mkdir(parents=True, exist_ok=True)
    requests_cache.install_cache(cache_name='corpus/raw_cache', backend='sqlite')

    # Посмотрим, что ждёт от нас сайт
    print('Содержимое robots.txt:', load_robots(root_url), sep='\n')

    # Получим список страниц для скачивания
    main_index = requests.get(urllib.parse.urljoin(root_url, 'politics/'))
    main_bs = bs4.BeautifulSoup(main_index.content.decode('utf-8'))
    # main_links = [link.get('href') for link in main_bs.find(name='div', attrs={'class': 'entry-content clearfix'}).find_all_next('a')]
    main_links = [(link.get('href'), link.get_text()) for link in main_bs.select('div.page__width a')]
    
    # Сохраним страницы
    content = []
    for link, title in tqdm(main_links):
        if link is not None and link[:4] == 'http':
            page_raw_text = requests.get(link).content
            with open((raw_root / title).with_suffix('.html'), 'wb') as dst:
                dst.write(page_raw_text)

            page_text = page_raw_text.decode('utf-8')
            page_bs = bs4.BeautifulSoup(page_text)
            # Все нормальные страницы (с оглавлением и заголовком h2)
#             page_content: bs4.element.Tag = page_bs.select_one('article h2 + p')
# #             print(page_content, page_bs)
#             if not page_content:
#                 # Хвост списка не содержит h2, но есть оглавление
#                 page_content: bs4.element.Tag = page_bs.select_one('article > div.page__width > p[style] + p')
#             if not page_content:
#                 # Странная страница "О", без h2 и оглавления
#                 page_content: bs4.element.Tag = page_bs.select_one('article > div.page__width > p')
#             if page_content is not None:
#                 content += list(map(str.strip, page_content.get_text().split('\n')))
#     print(len(content))
#     with open('corpus/cleaned.txt', 'w', encoding='utf-8') as dst:
#         for c in content:
#             print(c, file=dst)


if __name__ == "__main__":
    main()