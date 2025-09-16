from django.urls import path

from .views import ListArtist, DetailArtist, ListArtwork, DetailArtwork

urlpatterns = [
    path('artists/', ListArtist.as_view(), name='list_artist'),
    path('artists/<int:pk>/', DetailArtist.as_view(), name='detail_artist'),
    path('artworks/', ListArtwork.as_view(), name='list_artwork'),
    path('artworks/<int:pk>/', DetailArtwork.as_view(), name='detail_artwork'),
]