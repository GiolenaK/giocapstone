from django.shortcuts import render
from django.http import HttpResponse
from .models import PetProfile

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


def home(request):
    return render(request, 'pets/home.html')

def faq(request):
    return render(request, 'pets/faq.html')

def pet_list(request):
    pets = PetProfile.objects.all()  # Get all pets
    return render(request, 'pets/pets.html', {'pets': pets}) #send them to the pets.html
