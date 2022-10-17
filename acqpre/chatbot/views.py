import json

import django.db.utils
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .chatbot_ai import get_data, chat
from .models import Response, Rating, Tag


def index(request: HttpRequest):
    return render(request, "chatbot/index.html")


def api(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_response: Response = chat(data['user_input'])
        response = json.dumps(
            {'message': chat_response.text, 'tag': chat_response.tag.name, 'legal_basis': chat_response.legal_basis,
             'source': chat_response.source})
        return HttpResponse(response, content_type='application/json')
    return redirect('index')


def about(request: HttpRequest):
    return render(request, "chatbot/about.html")


def retrain(request: HttpRequest):
    get_data()
    return {'message': 'retraining'}


def rateResponse(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        tag = Tag.objects.get(name=data['responseTag'])
        response = Response.objects.get(tag=tag)
        try:
            Rating.objects.create(response=response, rating=data['rating'],
                                  ip=request.META.get("REMOTE_ADDR"))
        except django.db.utils.IntegrityError:
            rating = Rating.objects.get(response=response, ip=request.META.get("REMOTE_ADDR"))
            rating.rating = data['rating']
            rating.save()
        return HttpResponse(status='200')
    return redirect('index')
