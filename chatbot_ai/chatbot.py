import os

import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json

with open(os.path.join(os.path.dirname(__file__), "intents.json")) as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        _words = nltk.word_tokenize(pattern)
        words.extend(_words)
        docs_x.append(_words)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

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
    results = model.predict([bag_of_words(inp, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]
    responses = []
    for intent in data["intents"]:
        if intent["tag"] == tag:
            responses = intent["responses"]
            break
    return responses[random.randint(0, len(responses) - 1)]
