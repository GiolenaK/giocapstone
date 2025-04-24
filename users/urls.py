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
    path('staff/editpets/', views.edit_pets, name='edit-pets'),                   
    path('staff/editpets/<int:pk>/', views.edit_single_pet, name='edit-pet'),  
    path('staff/addpets/', views.add_pets, name='add-pets'),     
    path('staff/fosteringapplications/', views.fostering_applications, name='fostering-applications'),
    path('form-review/<str:application_id>/', views.form_review, name='form-review'),
    path('staff/addpetform/', views.add_pet_form, name='add-pet-form'),                      
    path('staff/badgeconfiguration/', views.badge_configuration, name='badge-configuration'),                   
    path('profile/upload-image/', views.upload_profile_image, name='upload-profile-image'),
    path('update-foster-status/', views.update_foster_status, name='update_foster_status'),
    path('pets/delete/<int:pk>/', views.delete_pet, name='delete-pet'),
    path('fosterform/', views.foster_request_view, name='foster-form'),
    path('mypets/',views.my_pets, name='my-pets'),

    
]
