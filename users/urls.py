from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user-index'),
    path('profile/', views.profile, name='user-profile'),
]
