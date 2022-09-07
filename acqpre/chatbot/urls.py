from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api, name='api'),
    path('about/', views.about, name='about'),
    path('retrain/', views.retrain, name='retrain'),
]