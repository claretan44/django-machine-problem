from django.test import TestCase
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