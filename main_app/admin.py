from django.contrib import admin
from .models import Pet, Profile, Place

# Register your models here.
admin.site.register(Place)
admin.site.register(Pet)
admin.site.register(Profile)
