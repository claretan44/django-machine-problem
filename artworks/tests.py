from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Artwork, Artist
# Create your tests here.

class ArtworkModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = Artist.objects.create(name="Artist",birth_year=1234,birth_place="Birth")
        cls.artwork = Artwork.objects.create(title='Artwork 1',year=4567, artist=cls.artist)

    def test_artist_model_content(self):
        self.assertEqual(self.artist.name, "Artist")
        self.assertEqual(self.artist.birth_year, 1234)
        self.assertEqual(self.artist.birth_place, "Birth")
        self.assertEqual(str(self.artist), "Artist")

    def test_artwork_model_content(self):
        self.assertEqual(self.artwork.title, "Artwork 1")
        self.assertEqual(self.artwork.year, 4567)
        self.assertEqual(self.artwork.artist.name, "Artist")
        self.assertEqual(str(self.artwork),"Artwork 1")

class ArtworkApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = Artist.objects.create(name="Artist",birth_year=1234,birth_place="Birth")
        cls.artwork = Artwork.objects.create(title='Artwork 1',year=4567, artist=cls.artist)
        cls.artwork_list_url = reverse('list_artwork')
        cls.artwork_detail_url = reverse('detail_artwork', args=[cls.artwork.id])
        cls.artist_list_url = reverse('list_artist')
        cls.artist_detail_url = reverse('detail_artist', args=[cls.artist.id])

    def test_list_artist(self):
        response = self.client.get(self.artist_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_list_artwork(self):
        response = self.client.get(self.artwork_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_detail_artist(self):
        response = self.client.get(self.artist_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Artist")
        self.assertEqual(response.data["birth_year"], 1234)
        self.assertEqual(response.data["birth_place"], "Birth")

    def test_detail_artwork(self):
        response = self.client.get(self.artwork_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Artwork 1")
        self.assertEqual(response.data["year"], 4567)
        self.assertEqual(response.data["artist"], self.artist.id)

    def test_detail_artist_not_found(self):
        response = self.client.get(reverse('detail_artist', args=[500]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_artwork_not_found(self):
        response = self.client.get(reverse('detail_artwork', args=[500]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)