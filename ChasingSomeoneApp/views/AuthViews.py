__author__ = 'charleszhuochen'
from django.shortcuts import render

def index(request):
    return render(request, 'ChasingSomeoneApp/index.html')

def login(request):
    return render(request, 'ChasingSomeoneApp/login.html')