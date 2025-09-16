from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    birth_place = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title