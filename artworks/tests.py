from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.test import TestCase, SimpleTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Artwork, Artist
# Create your tests here.

class IndexTest(SimpleTestCase):
    def test_url_exists(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

class ArtworkApiGetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        #setup done for the whole class, these objects will not be modified
        cls.artist = Artist.objects.create(name="Artist",birth_year=1234,birth_place="Birth")
        cls.artwork = Artwork.objects.create(title='Artwork 1',year=4567, artist=cls.artist)
        cls.artwork_list_url = reverse('list_artwork')
        cls.artwork_detail_url = reverse('detail_artwork', args=[cls.artwork.id])
        cls.artist_list_url = reverse('list_artist')
        cls.artist_detail_url = reverse('detail_artist', args=[cls.artist.id])

    def setUp(self):
        #setup of objects that will be modified, this runs per test
        self.test_artist = Artist.objects.create(name="Test_Artist",birth_year=1234,birth_place="Birth")
        self.test_artist_detail_url = reverse('detail_artist', args=[self.test_artist.id])
        self.test_artwork = Artwork.objects.create(title='Test_Artwork',year=4567, artist=self.test_artist)
        self.test_artwork_detail_url = reverse('detail_artwork', args=[self.test_artwork.id])

    #GET endpoints
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

    #Post Endpoint
    def test_create_artist(self):
        response = self.client.post(self.artist_list_url, data={'name': 'Test Create Artist', 'birth_year': 1234, 'birth_place': 'Birth'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_object = Artist.objects.get(pk=response.data["id"])
        self.assertEqual(created_object.name, "Test Create Artist")
        self.assertEqual(created_object.birth_year, 1234)
        self.assertEqual(created_object.birth_place, "Birth")

    def test_create_artwork(self):
        response = self.client.post(self.artwork_list_url, data={'title': 'Test Create Artwork', 'year': 4567, 'artist': self.test_artist.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_object = Artwork.objects.get(pk=response.data["id"])
        self.assertEqual(created_object.title, "Test Create Artwork")
        self.assertEqual(created_object.year, 4567)
        self.assertEqual(created_object.artist.id, self.test_artist.id)

    def test_create_artist_invalid(self):
        response = self.client.post(self.artist_list_url, data={'name': 'Test Create Artwork'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_artwork_invalid(self):
        response = self.client.post(self.artwork_list_url, data={'title': 'Test Create Artwork'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #PUT endpoint
    def test_update_artist_put(self):
        response = self.client.put(self.test_artist_detail_url, data={"name": "Updated Artist", "birth_place": "Updated Birth", "birth_year": 1245})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_artist.refresh_from_db()
        self.assertEqual(self.test_artist.name, "Updated Artist")
        self.assertEqual(self.test_artist.birth_place, "Updated Birth")
        self.assertEqual(self.test_artist.birth_year, 1245)

    def test_update_artwork_put(self):
        response = self.client.put(self.test_artwork_detail_url, data={"title": "Updated Artwork", "year": 4589, "artist" : self.test_artist.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_artwork.refresh_from_db()
        self.assertEqual(self.test_artwork.title, "Updated Artwork")
        self.assertEqual(self.test_artwork.year, 4589)
        self.assertEqual(self.test_artwork.artist.id, self.test_artist.id)

    def test_update_artist_put_invalid(self):
        response = self.client.put(self.test_artist_detail_url, data={"name": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_artwork_put_invalid(self):
        response = self.client.put(self.test_artwork_detail_url, data={"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #PATCH endpoint
    def test_update_artist_patch(self):
        response = self.client.patch(self.test_artist_detail_url, data={"name": "Updated Artist"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_artist.refresh_from_db()
        self.assertEqual(self.test_artist.name, "Updated Artist")

    def test_update_artwork_patch(self):
        response = self.client.patch(self.test_artwork_detail_url, data={"title": "Updated Artwork"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_artwork.refresh_from_db()
        self.assertEqual(self.test_artwork.title, "Updated Artwork")

    #DELETE endpoint

    def test_delete_artist(self):
        deleted_id = self.test_artist.id
        response = self.client.delete(self.test_artist_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Artist.objects.get(pk=deleted_id)

    def test_delete_artwork(self):
        deleted_id = self.test_artwork.id
        response = self.client.delete(self.test_artwork_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Artwork.objects.get(pk=deleted_id)
