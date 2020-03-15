#!.env/Scripts/python.exe

__doc__ = '''Скрипт очистки загруженных данных.'''

import bs4

from pathlib import Path
from tqdm import tqdm

def main():
    raw_root = Path('corpus/raw/')
    
    all_genre = ['Политика', 'В мире', 'Экономика', 'Общество', 'Происшествия',
                 'Армия', 'Наука', 'Культура', 'Религия', 'Спорт', 'Туризм']

    # Включаем кэшировие загруженных страниц
    clean_root = Path('corpus/clean')
    clean_root.mkdir(parents=True, exist_ok=True)

    # Пройдём по ранее скачанным страницам
    content = []
    for f in tqdm(raw_root.iterdir()):
        name_file = str(f)[len('corpus/raw/'):(len(str(f)) - len('.html'))]
        if f.suffix.lower() != '.html':
            continue

        with open(f, 'r', encoding='utf-8') as src:
            page_text = src.read()
            
        # Разберём страницу
        page_bs = bs4.BeautifulSoup(page_text)
        # Все нормальные страницы 
        page_content: bs4.element.Tag = page_bs.find_all(attrs={'class':'article__text'})
        page_genre: bs4.element.Tag = page_bs.find_all(attrs={'class':'article__tags'})
        
        # Определяем жанр новости
        for i in range(len(page_genre)):
            for genre_i in all_genre:
                if (genre_i in page_genre[i].get_text()):
                    genre = genre_i
                    break
            if (genre_i in page_genre[i].get_text()):
                genre = genre_i
                break

        # Вытаскиваем текст       
        if page_content is not None and genre is not None:
            one_content = []
            for i in range(1, len(page_content) - 1):
                one_content += list(map(str.strip, page_content[i].get_text().split('\n')))
                d = '\n'.join(one_content)
            content.append(d)

        with open(clean_root / genre /name_file, 'w', encoding='utf-8') as dst:
            c = d
            print(c, file=dst)

    print('Всего текстов:', len(content))
    
    with open(clean_root / 'data.txt', 'w', encoding='utf-8') as dst:
        for c in content:
            print(c, file=dst)


if __name__ == "__main__":
    main()