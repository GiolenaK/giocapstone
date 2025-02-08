from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    print("hellooooooo")
    return render(request, 'users/index.html')

def profile(request):
    random_user = {'username': 'Giolena'}
    random_user2 = {'username': 'Kat'}
    context = random_user
    return render(request, 'users/profile.html',{'user':context})