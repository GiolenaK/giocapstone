from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.pet, name='about'),
    path('needs/', views.needs, name='pet-needs'),
    path('toxic/', views.petstoxic, name='pet-toxic'),
    path('fosterer/', views.becomefosterer, name='become-fosterer'),
    path('fosterform/', views.fosterform, name='foster-form'),
    path('list/', views.pet_list, name='pet-list'),
    path('faq/', views.faq, name='faq'),
    path('list/', views.pet_list, name='pet-list'),
    path('contactus/', views.contact_us, name='contact'),
    path('favorite/<int:pet_id>/', views.toggle_favorite, name='toggle_favorite'),
]