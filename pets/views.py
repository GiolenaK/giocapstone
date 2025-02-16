from django.shortcuts import render
from django.http import HttpResponse

def pet(request):
    return render(request, 'pets/about.html')

def needs(request):
    return render(request, 'pets/petneeds.html')

def petstoxic(request):
    return render(request, 'pets/petstoxic.html')

def becomefosterer(request):
    return render(request, 'pets/becomefosterer.html')

def fosterform(request):
    return render(request, 'pets/fosteringform.html')


