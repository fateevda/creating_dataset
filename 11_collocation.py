#!.env/Scripts/python.exe

__doc__ = '''
Составляем списки словосочетаний по корпусу.
https://www.nltk.org/howto/collocations.html
'''

import logging
import math
from pathlib import Path

import nltk
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.corpus import stopwords
from nltk.corpus.reader import ConllCorpusReader
from tqdm import tqdm

from utils import setup_logger


_logger = logging.getLogger(__name__)


def t_score(n_ii, n_ind, n_xx) -> float:
    n_ix, n_xi = n_ind
    p0N = n_ix * n_xi / n_xx
    return (n_ii - p0N) / math.sqrt(n_ii)


def print_samples(bigram_finder: BigramCollocationFinder) -> None:
    """Печатаем в лог top-10 словосочетаний по разным метрикам"""
    # Метрики для биграмм
    bigram_measures = BigramAssocMeasures()

    # Найдём лучшие по разным метрика слосовочетания
    _logger.info('Лучшие с/с по PMI:')
    for i, collocation in enumerate(bigram_finder.nbest(bigram_measures.pmi, 20)):
        _logger.info('%02d. %s (%d)', i + 1, collocation, bigram_finder.ngram_fd[collocation])

    _logger.info('Лучшие с/с по t-score:')
    for i, collocation in enumerate(bigram_finder.nbest(t_score, 20)):
        _logger.info('%02d. %s (%d)', i + 1, collocation, bigram_finder.ngram_fd[collocation])

    _logger.info('Лучшие с/с по Dice:')
    for i, collocation in enumerate(bigram_finder.nbest(bigram_measures.dice, 20)):
        _logger.info('%02d. %s (%d)', i + 1, collocation, bigram_finder.ngram_fd[collocation])


def main() -> None:
    """Точка входа в приложение."""
    corpus_root = Path('corpus')
    # Настроим логирование результатов
    global _logger
    setup_logger(_logger, corpus_root / 'collocations.log')

    # Загрузим стоп-слова
    nltk.download('stopwords', '.env/share/nltk_data')
    stop_words = set(stopwords.words('russian'))

    # Импортируем корпус
    tags_root = corpus_root / 'pos_tagging'
    reader = ConllCorpusReader(str(tags_root), [f.name for f in tags_root.glob('*.tags')],
                               columntypes=['words', 'ignore', 'ignore', 'ignore', 'pos'],
                               separator='\t')
    _logger.info('Документов: %d', len(reader.fileids()))
    _logger.info('Токенов в первом документе (%s): %d',
                 reader.fileids()[0], len(reader.words(reader.fileids()[0])))

    _logger.info('Загружаем предложения')
    sentences = reader.sents()

    # Строим таблицы сопряжённости для всех слов в корпусе
    _logger.info('Считаем таблицу сопряжённости по всем словам')
    bigram_finder = BigramCollocationFinder.from_documents(
        [w.lower() for w in sent] for sent in tqdm(sentences))
    _logger.info('Всего биграм: %d', bigram_finder.N)

    print_samples(bigram_finder)

    # А теперь отфильтруем по частоте и удалим пунктуацию, стоп-слова
    _logger.info('Отфильтруем пунктуацию, стоп-слова и установим предел по частоте')
    bigram_finder.apply_freq_filter(5)
    bigram_finder.apply_word_filter(lambda w: len(w) < 3 or w in stop_words)
    _logger.info('Всего биграм: %d', bigram_finder.N)
    print_samples(bigram_finder)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        _logger.exception('Скрипт завершился с ошибкой')