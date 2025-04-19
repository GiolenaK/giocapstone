from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .utils import suggest_pets_for_user  
from .models import IdealPetProfile
from pets.models import Disability,PetProfile
from django.contrib import messages
from .forms import UserUpdateForm
from django.http import JsonResponse
from .forms import PetProfileForm
from django.shortcuts import render, get_object_or_404, redirect



from pets.choices import (FUR_CHOICES,
    SIZE_CHOICES,
    DOG_BREEDS,
    CAT_BREEDS,
    GENDER_CHOICES
)

from pets.models import (
    Disability,
    CharacterTrait,
    Allergy,
    )



@login_required(login_url='login')  # bug fix: when user was on sign up or login and they tried to access profile
def profile(request): #profile html page needs the foster and user status of the logged in user
    user = request.user  
    if user.user_type == "Admin":
        user_status = "Admin"
    elif user.user_type == "Staff":
        user_status = "Staff"
    elif user.user_type == "Simple": 
        if user.fosterer_status == "Accepted":
            user_status = "Fosterer"  
        else:
            user_status = "Simple User"  
    else:
        user_status = "Unknown"  

    return render(request, "users/profile.html", {"user_status": user_status})
def badge(request): # badge html page needs the foster and user status of the logged in user
    user = request.user 
    print(f"User: {user.username}, User Type: {user.user_type}, Fosterer Status: {user.fosterer_status}")

    user_type = user.user_type.lower() if user.user_type else ""

    if user_type == "admin":
        badge_status = "Admin"
    elif user_type == "staff":
        badge_status = "Staff"  #admin adn staff don't have accepted, rejected or pending in their badge
    else:  
        if user.fosterer_status == "Accepted":
            badge_status = "Accepted"
        elif user.fosterer_status == "Rejected":
            badge_status = "Rejected"
        elif user.fosterer_status == "Pending":
            badge_status = "Pending"
        else:
            badge_status = "None"  
    print(f"Assigned Badge: {badge_status}")


    return render(request, "users/badge.html", {"status": badge_status})


def user_login(request):

    if request.user.is_authenticated:  # if user is logged in and tries to access login page
        return redirect("user-profile")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user)  
            return redirect("home")  
        
        
        return render(request, "users/login.html", {"error": "Invalid username or password"})

    return render(request, "users/login.html")


def signup(request):

    if request.user.is_authenticated:  # if user is logged in and tries to access signup page
        return redirect("user-profile")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  #Redirect to home
        else:
            return render(request, "users/signup.html", {"form": form})  

    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/signup.html", {"form": form})

def logout_view(request): #simple logout function
    logout(request)
    return redirect("login")


@login_required
def user_profile(request):
    user = request.user
    suggested_pets = suggest_pets_for_user(user)  
    return render(request, 'users/profile.html', {
        'user': user,
        'suggested_pets': suggested_pets
    })


# users/views.py

@login_required
def edit_ideal_pet(request):
    profile, _ = IdealPetProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        return render(request, 'pets/pets.html', {
            'profile': profile,
            'disability_choices': Disability.objects.all(),
            'personality_choices': CharacterTrait.objects.all(),
            'allergy_choices': Allergy.objects.all(),
            'fur_choices': FUR_CHOICES,
            'size_choices': SIZE_CHOICES,
            'breed_choices': DOG_BREEDS + CAT_BREEDS,
            'gender_choices': GENDER_CHOICES,
        })
@login_required
def save_ideal_pet(request):
    

    if request.method == 'POST':
        profile, _ = IdealPetProfile.objects.get_or_create(user=request.user)

        profile.character_traits.clear()
        profile.disabilities.clear()
        profile.allergies.clear()
  
        # Simple Fields
        profile.gender = request.POST.get('ideal_gender') or None
        profile.fur = request.POST.get('ideal_fur') or None
        profile.size = request.POST.get('ideal_size') or None
        selected_breed = request.POST.get('ideal_breed') or None
        profile.species = request.POST.get('ideal_species') or None

        if selected_breed:
            dog_breeds_map = dict(DOG_BREEDS)
            cat_breeds_map = dict(CAT_BREEDS)

            if selected_breed in dog_breeds_map:
                profile.species = 'Dog'
                profile.dog_breed = selected_breed
                profile.cat_breed = None
            elif selected_breed in cat_breeds_map:
                profile.species = 'Cat'
                profile.cat_breed = selected_breed
                profile.dog_breed = None
            else:
                profile.dog_breed = None
                profile.cat_breed = None



        
        profile.age = request.POST.get('ideal_age') or None

        age_range = request.POST.get('ideal_age', '')
        if age_range:
            try:
                min_age, max_age = map(int, age_range.split("-"))
                profile.min_age = min_age
                profile.max_age = max_age
            except ValueError:
                profile.min_age = None
                profile.max_age = None
        else:
            # Clear the values if nothing selected
            profile.min_age = None
            profile.max_age = None
        # ManyToMany Fields
        trait_ids = [t for t in request.POST.getlist('ideal_personality') if t]
        disability_ids = [d for d in request.POST.getlist('ideal_disabilities') if d]
        allergy_ids = [a for a in request.POST.getlist('ideal_allergies') if a]


        if trait_ids:
            profile.character_traits.set(trait_ids)
        else:
            profile.character_traits.clear()

        if disability_ids:
            profile.disabilities.set(disability_ids)
        else:
            profile.disabilities.clear()

        if allergy_ids:
            profile.allergies.set(allergy_ids)
        else:
            profile.allergies.clear()

  
        profile.save()

        
        return redirect('/pets/list/')  
    
@login_required
def editprofile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('edit-profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/editprofile.html', {'form': form})


#to make the pfp instantly upload and preview
@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        user = request.user
        user.profile_photo = request.FILES['image']
        user.save()
        return redirect('edit-profile') 
    return redirect('edit-profile')

@login_required
def staff_panel(request):
    return render(request, 'users/staffpanel.html')


#just for loading up all the pets in the editpets html
@login_required
def edit_pets(request):
    pets = PetProfile.objects.all()
    return render(request, 'users/editpets.html', {'pets': pets})


#for editing single pets
@login_required
def edit_single_pet(request, pk):
    pet = get_object_or_404(PetProfile, pk=pk)

    if request.method == 'POST':
        form = PetProfileForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('edit-pets')
    else:
        form = PetProfileForm(instance=pet)

    return render(request, 'users/edit_single_pet.html', {'form': form, 'pet': pet})