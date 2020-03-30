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
    corpus_path = Path('corpus/super clean')

    cats = os.listdir(corpus_path)
    cat_size = [len(os.listdir(corpus_path / cat)) for cat in cats]

    for name, size in zip(cats, cat_size):
        print(name, size)

    our_cats = ['Наука', 'Экономика', 'Общество', 'Происшествия']


    # Корпус небольшой, можем себе позволить держать его в памяти.
    news = []
    target = []
    for i in range(len(our_cats)):
        for file in os.listdir(corpus_path / our_cats[i]):

            with open(corpus_path / our_cats[i] / file, 'r', encoding='utf-8') as src:
                text_news = ' '.join([line.rstrip('\r\n') for line in src])

            # x and y
            news.append(text_news)
            target.append(i)

    # stopwords
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stopWords = set(stopwords.words('russian'))

    # tokenizer
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    def preproc(text):
        return ' '.join([word for word in tokenizer.tokenize(text.lower()) if word not in stopWords])

    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=1300, preprocessor=preproc)

    vectors = vectorizer.fit_transform(news)
    vectors.shape

    dense_vectors = vectors.todense()

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import SGDClassifier
    from sklearn.metrics import accuracy_score

    svc = svm.SVC()
    sgd = SGDClassifier()
    print(f'Our categories: {our_cats}')
    X_train, X_test, y_train, y_test= train_test_split(dense_vectors, target, test_size=0.2)
    print(f'Size of train: {X_train.shape[0]}; Size of test {X_test.shape[0]}')

    sgd.fit(X_train, y_train)
    print(f'We have {len(our_cats)} categories. Accuracy:', accuracy_score(y_test, sgd.predict(X_test)))

if __name__ == "__main__":
    main()