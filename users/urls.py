from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/badge', views.badge, name='user-badge'),
    path('profile/edit', views.editprofile, name='edit-profile'),
    path('profile/staffpanel', views.staff_panel, name='staff-panel'),
    path('pets/editpets/', views.edit_pets, name='edit-pets'),                   
    path('pets/editpets/<int:pk>/', views.edit_single_pet, name='edit-pet'),    
    path('profile/upload-image/', views.upload_profile_image, name='upload-profile-image'),

    
]
