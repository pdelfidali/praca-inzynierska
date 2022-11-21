import numpy as np
import scipy.sparse.csr
import spacy
from sklearn import metrics
from sklearn.model_selection import train_test_split

from ..models import Tag, Pattern

nlp = spacy.load('pl_core_news_lg')


def get_data():
    from sklearn.feature_extraction.text import TfidfVectorizer

    X = []
    y = []
    labels = Tag.objects.all().values_list('name', flat=True)
    patterns = Pattern.objects.exclude(tag=None)
    for pattern in patterns:
        X.append(pattern.text)
        _labels = np.zeros(len(labels))
        _labels[pattern.tag_id - 1] = 1
        y.append(_labels)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123, stratify=y)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, max_features=150000)
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)
    return X_train, X_test, y_train, y_test


# def get_data_nn():
#     import tensorflow as tf
#     import tensorflow_transform as tft
#
#
#
#     X = []
#     y = []
#     labels = Tag.objects.all().values_list('name', flat=True)
#     patterns = Pattern.objects.exclude(tag=None)
#     for pattern in patterns:
#         X.append(pattern.text)
#         _labels = np.zeros(len(labels))
#         _labels[pattern.tag_id - 1] = 1
#         y.append(_labels)
#
#     VOCAB_SIZE = 250
#
#     tf.compat.v1.disable_eager_execution()
#
#     tokens = tf.compat.v1.string_split(X)
#     indices = tft.compute_and_apply_vocabulary(tokens, top_k=VOCAB_SIZE)
#     bow_indices, weight = tft.tfidf(indices, VOCAB_SIZE + 1)
#
#     vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, max_features=150000)
#     X = vectorizer.fit_transform(X)
#     X = np.array(X)
#     y = np.array(y)
#     return X, y


def printModelStats(base_accuracy, best_accuracy, model_name=None):
    if model_name:
        print(model_name.upper())
    print(f'Accuracy after grid search: {best_accuracy} vs accuracy of base model {base_accuracy}')
    print('Improvement of {:0.2f}%.'.format(100 * (best_accuracy - base_accuracy) / base_accuracy))
    print('\n\n\n\n')


def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    return metrics.accuracy_score(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1))