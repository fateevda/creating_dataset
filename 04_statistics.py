#!.env/Scripts/python.exe

__doc__ = '''Скрипт для подчёта статистики.'''

from pathlib import Path
from typing import List
from collections import Counter


def main() -> None:
    """Точка входа"""
    corpus_root = Path('corpus')
    # Читаем данные корпуса
    with open(corpus_root /'clean' / 'data.txt', 'r', encoding='utf-8') as src:
        news = [line.rstrip('\r\n') for line in src]
    # Считаем статистику
    with open(corpus_root / 'statistics.txt', 'w', encoding='utf-8') as dst:
        print('Всего новостей:', len(news), file=dst)

        words: List[str] = [w.lower().strip('.,') for p in news for w in p.split()]
        print('Всего слов:', len(words), file=dst)
        unique_words = Counter(words)
        print('Уникальных слов (токенов):', len(unique_words), file=dst)
        print('Самые частотные слова (токены):', file=dst)
        for i, (w, freq) in enumerate(unique_words.most_common(5)):
            print(f'\t{i}. {w} -> {freq}', file=dst)
        
        print('Количество символов (включая пробелы):',
              sum(len(p) for p in news), file=dst)


if __name__ == "__main__":
    main()