from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def index(request):
    print("hellooooooo")
    return render(request, 'users/index.html')

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

def editprofile(request):
   return render(request, 'users/editprofile.html')

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