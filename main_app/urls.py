from django.urls import path
from . import views
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
	
urlpatterns = [
	path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
]