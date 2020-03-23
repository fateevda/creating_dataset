#!.env/Scripts/python.exe

__doc__ = '''Скрипт для построения поискового индекса.'''

import os
from pathlib import Path
from typing import Iterable

import whoosh
import whoosh.writing
from whoosh.fields import TEXT, NUMERIC

from tqdm import tqdm


def add_to_index(news: Iterable[str],
                 idx_writer: whoosh.writing.IndexWriter) -> None:
    """Функция добавления в индекс"""
    for i, text in enumerate(news):
        idx_writer.add_document(text_id=i, text=text)

def file_searcher(path):
    """Находим названия всех файлов"""
    list_files = []
    for address, _, files in os.walk(path):
        for file in files:
            if file != 'data.txt':
                list_files.append((address + '/' +  file))
    return list_files  
        
def main() -> None:
    """Точка входа в приложение"""
    # Создаём папку с индексом
    print('Создаём папки...')
    root = Path('corpus')
    idx_dir = root / 'index'
    idx_dir.mkdir(parents=True, exist_ok=True)

    # Открываем корпус
    corpus_root = Path('corpus/super clean')
    list_files = file_searcher(corpus_root)
    news = []
    for file in list_files:
        with open(file, 'r', encoding='utf-8') as src:
            text_news = ' '.join([line.rstrip('\r\n') for line in src])
        news.append(text_news)    
    
    # Открываем и заполняем индекс
    print('Заполняем индекс')
    text_analyser = whoosh.analysis.StandardAnalyzer(stoplist=None, minsize=None) \
        | whoosh.analysis.StemFilter(lang='ru')
    schema = whoosh.fields.Schema(text_id=NUMERIC(unique=True, stored=True),
                                  text=TEXT(analyzer=text_analyser))
    idx = whoosh.index.create_in(idx_dir, schema)
    with idx.writer(procs=os.cpu_count()) as idx_writer:
        add_to_index(tqdm(news), idx_writer)
    
    print('Готово.')


if __name__ == "__main__":
    main()
