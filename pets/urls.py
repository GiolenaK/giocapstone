from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.pet, name='about'),
    path('needs/', views.needs, name='pet-needs'),
    
]