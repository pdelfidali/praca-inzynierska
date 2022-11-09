import numpy as np
import spacy
import tensorflow as tf
import tflearn
from nltk.stem.lancaster import LancasterStemmer

from .models import Tag, Pattern, Response

stemmer = LancasterStemmer()
nlp = spacy.load('pl_core_news_lg')
model = None
words = None
THRESHOLD = 0.5
UNDER_THRESHOLD_TAG = 'nierozpoznane zapytanie'


def get_data():
    train_model()


def process_message(text):
    return nlp(text).vector


def train_model():
    X = []
    y = []
    labels = Tag.objects.exclude(name='nierozpoznane zapytanie').values_list('id', flat=True).distinct()
    labels_zeros = [0 for _ in range(Tag.objects.count())]

    for tag in Tag.objects.exclude(name='nierozpoznane zapytanie'):
        for pattern in Pattern.objects.filter(tag=tag):
            X.append(process_message(pattern.text))
            _labels = labels_zeros
            _labels[tag.id] = 1
            y.append(_labels)
    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(X[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(labels), activation="softmax")
    net = tflearn.regression(net)

    global model
    model = tflearn.DNN(net)

    X = np.array(X)
    y = np.array(y)

    model.fit(X, y, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def chat(inp):
    if not model:
        train_model()
    x = np.array(process_message(inp)).reshape((1, 300))
    results = model.predict(x)
    print(results)
    if np.max(results) > THRESHOLD:
        results_index = np.argmax(results)
        tag = Tag.objects.get(id=results_index)
        x = Response.objects.get(tag=tag)
        return x
    else:
        pers_names = []
        doc = nlp(inp)
        text = doc.text
        for ent in doc.ents:
            if ent.label_ == "persName":
                pers_names.append(ent.text)
        if pers_names:
            for persName in pers_names:
                text = text.replace(persName, "Imię Nazwisko")
        pattern = Pattern(text=text)
        pattern.save()
        return Response.objects.get(tag__name=UNDER_THRESHOLD_TAG)
