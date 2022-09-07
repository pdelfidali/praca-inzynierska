import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from chatbot_ai.chatbot import chat


def index(request: HttpRequest):
    return render(request, "chatbot/index.html")


def api(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        response = json.dumps({'message': chat(data['user_input'])})
        return HttpResponse(response, content_type='application/json')
    return redirect('index')


def about(request: HttpRequest):
    return render(request, "chatbot/about.html")
