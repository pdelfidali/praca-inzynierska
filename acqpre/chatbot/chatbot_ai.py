import numpy as np
import spacy
from nltk.stem.lancaster import LancasterStemmer
from sklearn import preprocessing

from .ml.models import neuralnetwork
from .models import Tag, Pattern, Response

stemmer = LancasterStemmer()
label_encoder = preprocessing.LabelEncoder()
nlp = spacy.load('pl_core_news_lg')
model = None
words = None
THRESHOLD = 0.5
UNDER_THRESHOLD_TAG = 'nierozpoznane zapytanie'

label_dict = {}


def get_data():
    train_model()


def process_message(text):
    return nlp(text).vector


def train_model():
    global label_dict




def chat(user_input):
    global label_dict
    if not model:
        train_model()
    x = np.array(process_message(user_input)).reshape((1, 300))
    results = model.predict(x)
    if np.max(results) > THRESHOLD:
        results_index = np.argmax(results)
        tag = Tag.objects.get(name=label_dict[results_index])
        x = Response.objects.get(tag=tag)
        return x
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
