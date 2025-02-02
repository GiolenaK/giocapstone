from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    print("hellooooooo")
    return render(request, 'users/index.html')

def profile(request):
    print("hellooooooo")
    return render(request, 'users/profile.html')