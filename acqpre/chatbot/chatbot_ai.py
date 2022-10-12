import nltk
import numpy as np
import tensorflow as tf
import tflearn
from nltk.stem.lancaster import LancasterStemmer

from .models import Tag, Pattern, Response

stemmer = LancasterStemmer()
model = None
labels = None
words = None


def train_model():
    global model, labels, words

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for tag in Tag.objects.all():
        for pattern in Pattern.objects.filter(tag=tag):
            _words = nltk.word_tokenize(pattern.text)
            words.extend(_words)
            docs_x.append(_words)
            docs_y.append(tag.name)

        if tag.name not in labels:
            labels.append(tag.name)

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        _words = [stemmer.stem(w) for w in doc]

        for word in words:
            if word in _words:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, _words):
    _bag = [0 for _ in range(len(_words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(_word.lower()) for _word in s_words]

    for se in s_words:
        for i, w in enumerate(_words):
            if w == se:
                _bag[i] = 1

    return np.array(_bag)


def chat(inp):
    if not model:
        train_model()
    results = model.predict([bag_of_words(inp, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]
    x = Response.objects.get(tag__name=tag)
    return x


def get_data():
    train_model()
