import uuid
import boto3
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Place, Pet, Profile, Review, Photo, Favourite
from .forms import PetForm
from django.urls import reverse
import os
import requests
from django.contrib import messages
from django.db.models import Avg


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def places_index(request):
  selected_category = request.GET.get('selected_category', '')
  places = Place.objects.all()

  if selected_category:
     places = places.filter(category=selected_category)

  categories = Place.objects.values_list('category', flat=True).distinct()
  
  context = {
     'selected_category': selected_category,
     'places': places,
     'categories': categories,
  }

  return render(request, 'places/index.html', context)

@login_required
def profile_details(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  user = request.user
  pets = Pet.objects.filter(profile=profile)
  pet_form = PetForm()
  favourites = Favourite.objects.filter(user=request.user)
  contributions = profile.contributions
  
  context = {
    'profile': profile,
    'user': user,
    'pets': pets,
    'pet_form': pet_form,
    'favourites': favourites,
    'contributions': contributions
  }
  return render(request, 'profiles/profile_details.html', context)

class PetCreate(LoginRequiredMixin, CreateView):
  model = Pet
  fields = ['name', 'breed']

  def form_valid(self, form):
    form.instance.profile = self.request.user.profile
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse('profile_details', kwargs={'profile_id': self.object.profile.id})

class PetEditView(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = ['name', 'breed']

  def get_success_url(self):
    return reverse('profile_details', kwargs={'profile_id': self.object.profile.id})

class PetDeleteView(LoginRequiredMixin, DeleteView):
  model = Pet
  success_url = '/profiles/{profile_id}' 

@login_required
def search_city(request):
  context = {
      'GOOGLE_PLACES_API_KEY': os.environ.get('GOOGLE_PLACES_API_KEY'),
  }
  if request.method == 'POST':
      city = request.POST.get('city')
      lat = request.POST.get('lat')
      lng = request.POST.get('lng')
      if city and lat and lng:
          profile = Profile.objects.get(user=request.user)
          profile.city = city
          profile.latitude = float(lat)
          profile.longitude = float(lng)
          profile.save()
          return redirect('profile_details', profile_id=profile.id)

  return render(request, 'main_app/search_city.html', context)

@login_required
def add_place(request):
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        place_type = request.POST.get('place_type')
        if place_id:
            api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
            url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
            response = requests.get(url)
            data = response.json()

            if data['status'] == 'OK':
                place = data['result']
                name = place['name']
                address = place['formatted_address']
                city = None

                for component in place['address_components']:
                    if 'locality' in component['types']:
                        city = component['long_name']
                        break

                profile = Profile.objects.get(user=request.user)
                new_place = Place(name=name, address=address, category=place_type, city=city)
                # Increment contributions
                increment_contributions(request.user)

                new_place.save()

                return redirect('index')

            else:
                messages.error(request, 'Failed to fetch establishment details.')

    context = {
        'user_city': request.user.profile.city,
        'user_lat': request.user.profile.latitude,
        'user_lng': request.user.profile.longitude,
    }
    return render(request, 'main_app/add_place.html', context)

@login_required
def place_details(request, place_id):
  place = Place.objects.get(pk=place_id)
  review = Review.objects.filter(place=place)
  is_favourite = Favourite.objects.filter(user=request.user, place=place).exists()
  avg_rating = place.review_set.aggregate(Avg('rating'))['rating__avg']


  context = {
     'place': place,
     'review': review,
     'is_favourite': is_favourite,
     'avg_rating': avg_rating,
  }
  return render(request, 'places/details.html', context)

@login_required
def add_favourite(request, place_id):
    place = Place.objects.get(id=place_id)
    Favourite.objects.create(user=request.user, place=place) 
    return redirect('place_details', place_id=place_id)

@login_required
def remove_favourite(request, place_id):
    place = Place.objects.get(id=place_id)
    favourite = Favourite.objects.filter(user=request.user, place=place)
    favourite.delete()
    return redirect('place_details', place_id=place_id)


class ReviewCreate(LoginRequiredMixin, CreateView):
   model = Review
   fields = ['comment', 'rating']

   def form_valid(self, form):
    form.instance.place = Place.objects.get(pk=self.kwargs['place_pk'])
    form.instance.profile = self.request.user.profile
    return super().form_valid(form)

   def get_success_url(self):
      return reverse('place_details', kwargs={'place_id': self.object.place.id})
   

@login_required
def add_photo(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
  
    if pet.photos.count() >= pet.photos_limit:
      messages.error(request, 'Photo limit reached')
      return redirect('profile_details', profile_id=request.user.profile.id) 

    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, pet_id=pet_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)

    return redirect('profile_details', profile_id=request.user.profile.id)

@login_required
def delete_photo(request, pet_id, photo_id):
    photo = Photo.objects.get(id=photo_id)
    pet = photo.pet
    s3 = boto3.client('s3')
    key = photo.url.split('/')[-1]
    bucket = os.environ['S3_BUCKET']
    s3.delete_object(Bucket=bucket, Key=key)
    photo.delete()
    return redirect('profile_details', profile_id=pet.profile.id)


def increment_contributions(user):
  profile = Profile.objects.get(user=user)
  profile.contributions += 1
  profile.save()