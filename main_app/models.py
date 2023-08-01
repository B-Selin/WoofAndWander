from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    contributions  = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('profile_details', kwargs={'profile_id': self.id})

class Pet(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    


