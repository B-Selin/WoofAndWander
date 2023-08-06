from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

#  "place.category", (("amenity_1", "Amenity 1"), ("amenity_1", "Amenity 1"))
AMENITY_CHOICES = [
    ("airport", (
        ("potty_location", "Potty Location"),
        ("water", "Water"),
    )),
    ("amusement_park", (
        ("potty_location", "Potty Location"),
        ("water", "Water"),
        ("dog_friendly_rides", "Dog-Friendly Rides"),
    )),
    ("aquarium", (
        ("potty_location", "Potty Location"),
        ("water", "Water"),
    )),
    ("art_gallery", (
        ("potty_location", "Potty Location"), 
        ("water", "Water"),
        ("pet_friendly_exhibits", "Pet-Friendly Exhibits"),
    )),
    ("bakery", (
        ("dog_treats", "Dog Treats"),
        ("outdoor_seating", "Outdoor Seating"),
    )),
    ("cafe", (
        ("dog_treats", "Dog Treats"),
        ("outdoor_seating", "Outdoor Seating"),
        ("peaceful_walking_area", "Peaceful Walking Area"),
    )),
    ("park", (
        ("off_leash_area", "Off-Leash Area"),
        ("peaceful_walking_area", "Peaceful Walking Area"),
        ("waste_bags", "Waste Bags"),
        ("water", "Water"),
    )),
    ("beach", (
        ("off_leash_area", "Off-Leash Area"),
        ("water", "Water"),
        ("waste_bags", "Waste Bags"),
    )),
    ("campground", (
        ("off_leash_area", "Off-Leash Area"),
        ("peaceful_walking_area", "Peaceful Walking Area"),
        ("waste_bags", "Waste Bags"),
    )),
    ("pet_store", (
        ("dog_treats", "Dog Treats"),
        ("pet_supplies", "Pet Supplies"),
    )),
    ("vet_clinic", (
        ("dog_friendly_waiting_area", "Dog-Friendly Waiting Area"),
        ("pet_healthcare", "Pet Healthcare"),
    )),
    ("grooming_salon", (
        ("dog_grooming_services", "Dog Grooming Services"),
    )),
]



# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=255)
    amenities = models.ManyToManyField('Amenity', related_name='places')

    def __str__(self):
        return f'{self.name} ({self.id})'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    contributions  = models.IntegerField(default=0)
    favourites = models.ManyToManyField(Place)

    def __str__(self): 
        return f'{self.user} ({self.id})'
    def get_absolute_url(self):
        return reverse('profile_details', kwargs={'profile_id': self.id})

class Pet(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    photos_limit = models.IntegerField(default=3)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pets')
    
    def __str__(self): 
        return f'{self.name} ({self.id})'


class Photo(models.Model):
    url = models.CharField(max_length=200)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return f'Photo for{self.pet_id} @{self.url}'

    
class Review(models.Model):
    comment = models.TextField(max_length=150)
    rating = models.IntegerField(default=5)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'place')

    # def __str__(self):
    #     return f'{self.place.name} favourited by {self.profile.user}'

class Amenity(models.Model):
    name = models.CharField(max_length=50, choices=AMENITY_CHOICES)
    
    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    vote = models.BooleanField()