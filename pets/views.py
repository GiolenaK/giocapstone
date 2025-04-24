from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from .models import PetProfile
from users.utils import suggest_pets_for_user
from users.models import DOG_BREEDS, CAT_BREEDS, SIZE_CHOICES, GENDER_CHOICES,FUR_CHOICES, SPECIES_CHOICES
from django.contrib.auth.decorators import login_required
from pets.models import PetProfile, FavoritedPet
from users.models import IdealPetProfile
from django.db.models import Q
from .models import CharacterTrait, Disability  
from django.core.mail import send_mail
from django.urls import reverse
import random



#simple rendering functions
def pet(request):
    return render(request, 'pets/about.html')

def needs(request):
    return render(request, 'pets/petneeds.html')

def petstoxic(request):
    return render(request, 'pets/petstoxic.html')

def becomefosterer(request):
    return render(request, 'pets/becomefosterer.html')

def faq(request):
    return render(request, 'pets/faq.html')


#rendering page but also adding three random pets from database
def home(request):
    pets = list(PetProfile.objects.exclude(image=''))  
    random_pets = random.sample(pets, min(3, len(pets))) 
    return render(request, 'pets/home.html', {'random_pets': random_pets})




#lots of stuff
#search queries for searchbar
#filtering for the filter popup
#loading up favorites, ideal pets, and all pets

def pet_list(request):
    pets = PetProfile.objects.all()
    search_query = request.GET.get("search", "")

    #for the search bar, search terms
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(species__icontains=search_query) |
            Q(size__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(age__icontains=search_query) |
            Q(character_traits__name__icontains=search_query) |
            Q(allergies__name__icontains=search_query) |
            Q(disabilities__name__icontains=search_query)|
            Q(fur__icontains=search_query)
  
        ).distinct() 


    #for the small filter system
    breed = request.GET.get("breed")
    size = request.GET.get("size")
    gender = request.GET.get("gender")
    age_range = request.GET.get("age")
    

    if breed:
        pets = pets.filter(breed__iexact=breed)

    if size:
        pets = pets.filter(size__iexact=size)

    if gender:
        pets = pets.filter(gender__iexact=gender)

    if age_range:
        min_age, max_age = map(int, age_range.split("-"))
        pets = pets.filter(age__gte=min_age, age__lte=max_age)


    all_pets = PetProfile.objects.all()
    suggested_pets = None
    favorited_pets = []

    #additionally sections for suggested and faves are populated
    if request.user.is_authenticated:
        suggested_pets = suggest_pets_for_user(request.user)
        favorited_pets = FavoritedPet.objects.filter(user=request.user).select_related('pet')

    return render(request, 'pets/pets.html', {
        'pets': pets,
        'suggested_pets': suggested_pets,
        'size_choices': SIZE_CHOICES,
        'gender_choices': GENDER_CHOICES,
        'species_choices' : SPECIES_CHOICES,
        'breed_choices': DOG_BREEDS + CAT_BREEDS,
        'favorited_pets': [f.pet for f in favorited_pets],
        'personality_choices': CharacterTrait.objects.all(), 
        'fur_choices': FUR_CHOICES,
        'disability_choices': Disability.objects.all(),
        'request': request,
})

#assigns a favorite pet to a user
def toggle_favorite(request, pet_id):
    if not request.user.is_authenticated:
        return redirect('login')  

    pet = get_object_or_404(PetProfile, id=pet_id)
    favorite, created = FavoritedPet.objects.get_or_create(user=request.user, pet=pet)

    if not created:
        favorite.delete()

    return redirect('pet-list')  

#the format of the contact form that will be sent to the gmail
def contact_us(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        subject= request.POST.get('subject')
        message= request.POST.get('message')
        

        data = {
            'email': email,
            'subject': subject,
            'message': message,
        }   

        message = '''
        New Message: {}

        From: {}
        '''.format(data['message'], data['email'])
        send_mail(
            subject,
            message,
            email,
            ['giolenacapstone@gmail.com'],
            fail_silently=False,
        )
        return redirect(reverse('contact') + '?success=1')

    return render(request, 'pets/contact.html', {})

