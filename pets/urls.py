from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.pet, name='about'),
    path('needs/', views.needs, name='pet-needs'),
    path('toxic/', views.petstoxic, name='pet-toxic'),
    path('fosterer/', views.becomefosterer, name='become-fosterer'),
    path('fosterform/', views.fosterform, name='foster-form'),
    
]