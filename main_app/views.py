from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Place, Pet, Profile
from .forms import PetForm

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

@login_required
def places_index(request):
  places = Place.objects.all()
  return render(request, 'places/index.html', {'places': places})


def profile_details(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  user = profile.user
  pets = Pet.objects.filter(profile=profile)
  pet_form = PetForm()
  context = {
    'profile': profile,
    'user': user,
    'pets': pets,
    'pet_form': pet_form,
  }
  return render(request, 'profiles/profile_details.html', context)

# class PetCreate(LoginRequiredMixin, CreateView):
#   model = Pet
#   fields = '__all__'

def add_pet(request, profile_id):
  form = PetForm(request.POST)
  if form.is_valid():
    new_pet = form.save(commit=False)
    new_pet.user = request.user
    new_pet.profile_id = profile_id
    new_pet.save()
    return redirect('profile_details', profile_id=profile_id)
  
