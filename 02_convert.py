#!.env/Scripts/python.exe

__doc__ = '''Скрипт очистки загруженных данных.'''

import bs4

from pathlib import Path
from tqdm.notebook import tqdm

def main():
    raw_root = Path('corpus/raw/')
    
    all_genre = ['Политика', 'В мире', 'Экономика', 'Общество', 'Происшествия',
                 'Армия', 'Наука', 'Культура', 'Религия', 'Спорт', 'Туризм']

    # Включаем кэшировие загруженных страниц
    clean_root = Path('corpus/clean')
    clean_root.mkdir(parents=True, exist_ok=True)
    
    # Создаем пустые папки
    import os
    for genre in all_genre:
        if not os.path.exists(clean_root / genre):
            os.makedirs(clean_root / genre)

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
        
        #Определяем жанр новости
        for i in range(len(page_genre)):
            find_genre = False
            
            for genre_i in all_genre:
                if (genre_i in page_genre[i].get_text()):
                    genre = genre_i
                    find_genre = True
                    break
                    
            if find_genre:
                break
        
        # Вытаскиваем текст       
        if page_content is not None and genre is not None and page_content != []:
                    
            # Первую часть обрезаем до точки (ВАШИНГТОН, 14 мар – РИА Новости)
            start_flag = 'РИА Новости'
            start_text = page_content[0].get_text()
            
            if start_flag in start_text:
                
                one_content = [start_text[start_text.index('.') + 1:].strip()] 

                for i in range(1, len(page_content)):
                    one_content += list(map(str.strip, page_content[i].get_text().split('\n')))

                post = '\n'.join(one_content)
                content.append(' '.join(one_content))

                # Записываем наши новости по папкам
                with open(clean_root / genre / name_file, 'w', encoding='utf-8') as dst:
                    print(post, file=dst)
            
            
    print('Всего текстов:', len(content))
    
    with open(clean_root / 'data.txt', 'w', encoding='utf-8') as dst:
        print('\n'.join(content), file=dst)


if __name__ == "__main__":
    main()