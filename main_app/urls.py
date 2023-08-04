from django.urls import path
from . import views
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
	
urlpatterns = [
	# path('', views.home, name='home'),
    path('', views.landing, name='landing'),
    path('accounts/signup/', views.signup, name='signup'),
    path('places/', views.places_index, name='index'),
    path('places/<int:place_id>', views.place_details, name='place_details'),
    # route for the add favourite
    path('places/<int:place_id>/add_favourite/', views.add_favourite, name='add_favourite'),
    path('places/<int:place_id>/remove_favourite/', views.remove_favourite, name='remove_favourite'),
    path('profiles/<int:profile_id>', views.profile_details, name='profile_details'),
    path('pets/create/<int:profile_id>/', views.PetCreate.as_view(), name='pet_create'),
    path('pets/<int:pk>/edit/', views.PetEditView.as_view(), name='pet_edit'),
    path('pets/<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet_delete'),
    # route for the pet add_photo
    path('pets/<int:pet_id>/add_photo/', views.add_photo, name='add_photo'),
    # route for the pet delete_photo
    path('pets/<int:pet_id>/delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('places/<int:place_pk>/review/create/', views.ReviewCreate.as_view(), name='review_create'),    
    path('search_city/', views.search_city, name='search_city'),
    path('add_place/', views.add_place, name='add_place'),
]