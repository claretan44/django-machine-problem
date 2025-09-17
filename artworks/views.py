from rest_framework import generics

from .models import Artwork, Artist
from .serializers import ArtworkSerializer, ArtistSerializer
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'artworks/index.html')
class ListArtist(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class DetailArtist(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class ListArtwork(generics.ListCreateAPIView):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer

class DetailArtwork(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer