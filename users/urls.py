from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user-index'),
    path('login/', views.login, name='user-login'),
    path('signup/', views.signup, name='user-signup'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/badge', views.badge, name='user-badge'),
    path('profile/edit-profile', views.editprofile, name='user-edit-profile'),
]
