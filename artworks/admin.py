from django.contrib import admin
from .models import Artwork, Artist
# Register your models here.

admin.site.register(Artist)
admin.site.register(Artwork)
