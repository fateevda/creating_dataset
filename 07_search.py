#!.env/Scripts/python.exe

__doc__ = '''Скрипт для поиска по корпусу.'''

from pathlib import Path

import os
import whoosh.index
import whoosh.qparser
import whoosh.highlight

def file_searcher(path):
    """Находим названия всех файлов"""
    list_files = []
    for address, _, files in os.walk(path):
        for file in files:
            if file != 'data.txt':
                list_files.append((address + '/' +  file))
    return list_files 


def main() -> None:
    """Точка входа в приложение."""
    root = Path('corpus')
    
    # Подгружаем корпус (не храним тексты в индексе)
    corpus_root = Path('corpus/super clean')
    list_files = file_searcher(corpus_root)
    news = []
    for file in list_files:
        with open(file, 'r', encoding='utf-8') as src:
            text_news = '\n'.join([line.rstrip('\r\n') for line in src])
        news.append(text_news)    
    
    # Подгружаем индекс
    index_root = root / 'index'
    print('Загружаем индекс из', index_root)
    idx = whoosh.index.open_dir(index_root)
    
    # Парсер для запроса
    parser = whoosh.qparser.QueryParser('text', idx.schema)

    # Ввод самого запроса
    request = input('Введите запрос:')
    query = parser.parse(request)
    
    # Поиск
    with idx.searcher() as searcher:
        result = searcher.search(query, limit=None, terms=True)
    
        # Показываем результаты поиска
        hlt = whoosh.highlight.Highlighter(
            fragmenter=whoosh.highlight.WholeFragmenter(),
            formatter=whoosh.highlight.UppercaseFormatter())
        for hit in result:
            print(hlt.highlight_hit(hit, 'text', text=news[hit['text_id']]))
            print()
        
        print('"' + request + '"', 'встретилось в ', len(result), 'новостях')


if __name__ == "__main__":
    main()