#!.env/Scripts/python.exe

__doc__ = '''Скрипт для разметки корпуса частями речи.'''

from pathlib import Path
from collections import Counter
import os
import nltk
from tqdm import tqdm

def file_searcher(path):
    """Находим названия всех файлов"""
    list_files = []
    for address, _, files in os.walk(path):
        for file in files:
            if file != 'data.txt':
                list_files.append((address + '/' +  file))
    return list_files 


def main():
    """Точка входа."""
    corpus_root = Path('corpus')
    corpus_path = Path('corpus/super clean')
    tagged_root = corpus_root / 'pos_tagging'

    nltk_data_root = Path('.env/share/nltk_data')
    nltk_data_root.mkdir(parents=True, exist_ok=True)
    nltk.download('punkt', nltk_data_root)
    nltk.download('averaged_perceptron_tagger_ru')

    # Корпус небольшой, можем себе позволить держать его в памяти.
    list_files = file_searcher(corpus_path)
    news = []
    for file in list_files:
        with open(file, 'r', encoding='utf-8') as src:
            text_news = ' '.join([line.rstrip('\r\n') for line in src])
        news.append(text_news)

    # Сразу будем приводить к начальной форме (стеммингом) - для поиска
    stemmer = nltk.stem.snowball.SnowballStemmer('russian')

    print('Разобьём на предложения и слова')
    tagged_root.mkdir(exist_ok=True, parents=True)

    pos_stats = nltk.FreqDist()
    form_stats = nltk.FreqDist()
    for i, news in enumerate(tqdm(news)):
        offset = 0
        lower_news : str = news.lower()
        with open(tagged_root / f'{i}.tags', 'w', encoding='utf-8') as dst:
            for sent in nltk.sent_tokenize(news, language='russian'):
                words = nltk.word_tokenize(sent, language='russian', preserve_line=True)

                tagged = nltk.pos_tag(words, lang='rus')
                forms = list(map(stemmer.stem, words))

                # Считаем статистику по частям речи
                pos_stats.update(tag for w, tag in tagged)
                # Cчитаем статистиску по началльным формам
                form_stats.update(forms)

                # Сопоставим найденные слова с исходными координатами и сохраняем в файл
                for w, tag in tagged:
                    if w in ('``', "''"):
                        continue
                    word_offset = lower_news.find(w.lower(), offset)
                    assert word_offset >= 0, \
                    f"Не смогли восстановить координату слова {w} в исходном тексте: {news}"
                    print(w, word_offset, stemmer.stem(w), tag, sep='\t', file=dst)
                    offset = word_offset + len(w)

                # Пустой строкой разделяем предложения
                print(file=dst)

    # Отобразим статистику
    with open(corpus_root / 'pos_statistics.txt' , 'w', encoding='utf-8') as dst:
        print('Статистика по частям речи в корпусе:')
        for i, (pos, freq) in enumerate(pos_stats.most_common()):
            print(f'{i}. {pos} -> {freq} ({freq / pos_stats.N():.4f})')
            print(pos, freq, sep='\t', file=dst)

    print()       
    # Отобразим статистику
    with open(corpus_root / 'form_statistics.txt' , 'w', encoding='utf-8') as dst:
        print('Статистика по начальным формам в корпусе:')
        for i, (form, freq) in enumerate(form_stats.most_common(50)):
            print(f'{i}. {form} -> {freq} ({freq / form_stats.N():.4f})')
            print(form, freq, sep='\t', file=dst)



if __name__ == "__main__":
    main()
