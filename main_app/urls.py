from django.urls import path
from . import views
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
	
urlpatterns = [
	path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('places/', views.places_index, name='index'), 
    path('profiles/<int:profile_id>', views.profile_details, name='profile_details'),
    path('pets/create/<int:profile_id>/', views.PetCreate.as_view(), name='pet_create'),
    path('pets/<int:pk>/edit/', views.PetEditView.as_view(), name='pet_edit'),
    path('pets/<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet_delete'),    
]