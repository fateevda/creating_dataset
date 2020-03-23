#!.env/Scripts/python.exe

__doc__ = '''Скрипт для удаления дубликатов.'''

import os
import re
from pathlib import Path
from typing import List
from datasketch import MinHash, MinHashLSH


HASH_PERMUTATIONS_COUNT = 64


def normalize(text: str) -> List[str]:
    """Приводим строчки к детерминированному виду."""
    return re.sub(r'[^\w\s]', '', text).lower().split()


def to_minhash(words: List[str]) -> MinHash:
    """Сворачиваем текст в набор шинглов"""
    hasher = MinHash(num_perm=HASH_PERMUTATIONS_COUNT)
    for w in words:
        hasher.update(w.encode('utf-8'))
    return hasher

def file_searcher(path):
    """Находим названия всех файлов"""
    list_files = []
    for address, _, files in os.walk(path):
        for file in files:
            if file != 'data.txt':
                list_files.append((address + '/' +  file))
    return list_files

def main():
    """Точка входа в приложение."""
    corpus_root = Path('corpus/clean')
    
    """Находим названия всех файлов"""
    list_files = file_searcher(corpus_root)

    print('Загружаем корпус')
    raw_corpus = []
    for file in list_files:
        with open(file, 'r', encoding='utf-8') as src:
            text_news = '\n'.join([line.rstrip('\r\n') for line in src])
        raw_corpus.append(text_news)
   
    
    print('Приводим его к стандартному виду')
    normalized_copus: List[List[str]] = [normalize(news) for news in raw_corpus]

    print('Составляем индекс для поиска дублей')
    dst = open('duplicate.txt', 'w', encoding='utf-8')
    
    lsh = MinHashLSH(num_perm=HASH_PERMUTATIONS_COUNT)
    deduplicated_corpus = []
    for i, (file, words) in enumerate(zip(list_files, normalized_copus)):
        words_hash = to_minhash(words)
        duplicates = lsh.query(words_hash)
        if duplicates:
            print(f'Найдены совпадения для ({file}): {raw_corpus[i]}', file=dst)
            for idx in duplicates:
                print(f'\t{list_files[idx]}. {raw_corpus[idx]}', file=dst)
            print('\n\n\n\n', file=dst)
        else:
            lsh.insert(i, words_hash)
            deduplicated_corpus.append((raw_corpus[i], list_files[i]))
    print('Удалено дублей:', len(raw_corpus) - len(deduplicated_corpus), file=dst)

    print(f'Сохраняем дедуплицированный корпус ({len(deduplicated_corpus)} новостей)')
    
    # Создаем пустые папки
    all_genre = ['Политика', 'В мире', 'Экономика', 'Общество', 'Происшествия',
                 'Армия', 'Наука', 'Культура', 'Религия', 'Спорт', 'Туризм']
    import os
    for genre in all_genre:
        newpath = 'corpus/super clean/' + genre
        if not os.path.exists(newpath):
            os.makedirs(newpath)
    
    # Сохраняем корпус
    for text, name in deduplicated_corpus:
        with open('corpus/super clean/' + name[13:], 'w', encoding='utf-8') as dst:
            print(text, file=dst)

if __name__ == "__main__":
    main()