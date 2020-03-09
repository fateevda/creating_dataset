#!.env/Scripts/python.exe

__doc__ = '''Скрипт очистки загруженных данных.'''

import bs4

from pathlib import Path
from tqdm import tqdm

def main():
    raw_root = Path('corpus/raw/politics')

    # Включаем кэшировие загруженных страниц
    clean_root = Path('corpus/clean')
    clean_root.mkdir(parents=True, exist_ok=True)

    # Пройдём по ранее скачанным страницам
    content = []
#     qwer = 1
    for f in tqdm(raw_root.iterdir()):
        name_file = str(f)[len('corpus/raw/politics/'):(len(str(f)) - len('.html'))]
        
        if f.suffix.lower() != '.html':
            continue

        with open(f, 'r', encoding='utf-8') as src:
            page_text = src.read()
        
        # Разберём страницу
        page_bs = bs4.BeautifulSoup(page_text)
        # Все нормальные страницы 
        page_content: bs4.element.Tag = page_bs.find_all(attrs={'class':'article__text'})
            
            

        if page_content is not None:
            one_content = []
            for i in range(len(page_content) - 1):
                one_content += list(map(str.strip, page_content[i].get_text().split('\n')))
                d = ' '.join(one_content)
            content.append(d)
            
        with open(clean_root / name_file, 'w', encoding='utf-8') as dst:
            c = d
            print(c, file=dst)

    print('Всего текстов:', len(content))
    
    with open(clean_root / 'data.txt', 'w', encoding='utf-8') as dst:
        for c in content:
            print(c, file=dst)


if __name__ == "__main__":
    main()