import numpy as np
import spacy

nlp = spacy.load('pl_core_news_lg')

from nltk.stem.lancaster import LancasterStemmer
from sklearn import preprocessing

from .ml.helpers import get_data
from .ml.models import best_model
from .models import Tag, Pattern, Response

stemmer = LancasterStemmer()
label_encoder = preprocessing.LabelEncoder()

model = None
words = None
THRESHOLD = 0.4
UNDER_THRESHOLD_TAG = 'nierozpoznane zapytanie'
vectorizer = None

label_dict = {}


def process_message(text):
    return vectorizer.transform([text, ])


def train_model():
    global model, vectorizer
    X, y, vectorizer = get_data(False)
    model = best_model(X, y)


def chat(user_input):
    if not model:
        train_model()
    x = process_message(user_input)
    result_index = np.argmax(model.predict(x))
    probabilities = model.predict_proba(x)
    max_prob = probabilities[result_index][0][1]
    if max_prob >= THRESHOLD:
        tag = Tag.objects.get(id=result_index + 1)
        return Response.objects.get(tag=tag)
    else:
        pers_names = []
        doc = nlp(user_input)
        text = doc.text
        for ent in doc.ents:
            if ent.label_ == "persName":
                pers_names.append(ent.text)
        if pers_names:
            for persName in pers_names:
                text = text.replace(persName, "Imię Nazwisko")
        if text not in set(x[0] for x in Pattern.objects.all().values_list('text')):
            pattern = Pattern(text=text)
            pattern.save()
        return Response.objects.get(tag__name=UNDER_THRESHOLD_TAG)
