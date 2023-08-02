from django.urls import path
from . import views
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
	
urlpatterns = [
	path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('places/', views.places_index, name='index'),
    path('places/<int:place_id>', views.place_details, name='place_details'),
    path('profiles/<int:profile_id>', views.profile_details, name='profile_details'),
    path('pets/create/<int:profile_id>/', views.PetCreate.as_view(), name='pet_create'),
    path('pets/<int:pk>/edit/', views.PetEditView.as_view(), name='pet_edit'),
    path('pets/<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet_delete'),
    # route for the pet add_photo
    path('pets/<int:pet_id>/add_photo/', views.add_photo, name='add_photo'),
    path('places/<int:place_pk>/review/create/', views.ReviewCreate.as_view(), name='review_create'),    
    path('search_city/', views.search_city, name='search_city'),
    path('add_place/', views.add_place, name='add_place'),
]