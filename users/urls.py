from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user-index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/badge', views.badge, name='user-badge'),
    path('profile/edit', views.editprofile, name='user-edit-profile'),
]
