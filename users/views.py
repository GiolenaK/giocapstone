from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    print("hellooooooo")
    return render(request, 'users/index.html')

def profile(request):
    usertype1 = {'status': 'Fosterer'}
    usertype2 = {'status': 'Admin'}
    usertype3 = {'status': 'Staff'}
    context = usertype1
    return render(request, 'users/profile.html',{'user':context})

def badge(request):
    badgestatus1 = {'status': 'Accepted'}
    badgestatus2 = {'status': 'Pending'}
    badgestatus3 = {'status': 'Rejected'}
    badgestatus4 = {'status': 'Admin'}
    badgestatus5 = {'status': 'Staff'}
    badgestatus6 = {'status': 'None'}
    context = badgestatus1
    return render(request, 'users/badge.html',{'status':context})
   
