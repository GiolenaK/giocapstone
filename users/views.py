from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
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
from .models import CustomUser
from django.db.models import Q
from .models import FosteringApplication
from pets.choices import (FUR_CHOICES,SIZE_CHOICES,DOG_BREEDS,CAT_BREEDS,GENDER_CHOICES,SPECIES_CHOICES)
from pets.models import (Disability,CharacterTrait,Allergy)



@login_required  # bug fix: when user was on sign up or login and they tried to access profile
def profile(request): #profile html page needs the foster and user status of the logged in user
    user = request.user  
    user_type = user.user_type
    fosterer_status= None

    if user_type == "Simple":
         fosterer_status = user.fosterer_status or "none"


    return render(request, "users/profile.html", {'user': user, "user_type": user_type, 'fosterer_status': fosterer_status})

@login_required 
def badge(request): # badge html page needs the foster and user status of the logged in user
    user = request.user 
    fosterer_status = user.fosterer_status or "none"

    print(f"User: {user.username}, User Type: {user.user_type}, Fosterer Status: {user.fosterer_status}")
    return render(request, "users/badge.html", {'user': user, 'fosterer_status': fosterer_status})



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
            'species_choices': SPECIES_CHOICES,
        })

@login_required
def save_ideal_pet(request):
    if request.method == 'POST':
        profile, _ = IdealPetProfile.objects.get_or_create(user=request.user)

        profile.character_traits.clear()
        profile.disabilities.clear()
        profile.allergies.clear()
  
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
            
            profile.min_age = None
            profile.max_age = None

        # many to many, these use tags
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



#only editable badges are for users who AREN'T admin or staff
@login_required
def badge_configuration(request):
    users = CustomUser.objects.exclude(Q(user_type='admin') | Q(user_type='staff'))
    return render(request, 'users/badgeconfiguration.html', {'users': users, 'user_fosterer_status': CustomUser.FOSTERER_STATUS_CHOICES,})

@login_required
def update_foster_status(request):
    if request.method == "POST":
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            new_status = request.POST.get("fosterer_status")

            try:
                user = CustomUser.objects.get(pk=user_id)
                user.fosterer_status = new_status
                user.save()
            except CustomUser.DoesNotExist:
                print("User not found.")
    print(request.POST)
    return redirect('badge-configuration')


#just to load the table of all pets
@login_required
def add_pets(request):
    pets = PetProfile.objects.all()
    return render(request, 'users/addpet.html', {'pets': pets})

#this loads the form to add pets and fills things like dropdowns with info from the petprofileform
@login_required
def add_pet_form(request):
    if request.method == "POST":
        form = PetProfileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('add-pets')
        else:
            print("Form errors:", form.errors)

    else:
        form = PetProfileForm()
    return render(request, "users/addpetform.html", {"form": form})

@login_required
def delete_pet(request, pk):
    pet = get_object_or_404(PetProfile, pk=pk)
    pet.delete()
    return redirect('edit-pets')



@login_required
def foster_request_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        date_of_birth = request.POST.get('dob')
        address = request.POST.get('address')
        phone_number = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        proof_of_identity = request.FILES.get('proofOfIdentity')
        proof_of_residence = request.FILES.get('proofOfResidence')
        prior_experience = request.POST.get('priorExperience')

        # save and bind to user thats logged in
        FosteringApplication.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            address=address,
            phone_number=phone_number,
            email=email,
            proof_of_identity=proof_of_identity,
            proof_of_residence=proof_of_residence,
            prior_experience=prior_experience
        )

        return redirect('become-fosterer')

    return render(request, 'pets/fosteringform.html')


#just display the submitted applications
@login_required
def fostering_applications(request):
    forms = FosteringApplication.objects.filter()
    return render(request, 'users/fosteringapplications.html', {'forms': forms})

#similar to previous, just loads the data of the specific application the staff selected
@login_required
def form_review(request, application_id):
    form = get_object_or_404(FosteringApplication, id=application_id)

    return render(request, 'users/formreview.html', {'form': form})


@login_required
def my_pets(request):
    return render(request, 'users/mypets.html')
