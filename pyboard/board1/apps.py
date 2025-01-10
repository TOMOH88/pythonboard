from django.apps import AppConfig
from django.shortcuts import render

class Board1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board1'


def home(request):
    return render(request, 'home.html')
