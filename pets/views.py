from django.shortcuts import render
from django.http import HttpResponse

def pet(request):
    return render(request, 'pets/about.html')

def needs(request):
    return render(request, 'pets/petneeds.html')


