from rest_framework import serializers

from .models import Artist, Artwork

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'name',
            'birth_year',
            'birth_place',
        )

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = (
            'id',
            'title',
            'year',
            'artist',
        )