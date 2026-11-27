from psycopg2 import IntegrityError

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('post_install', '-at_install')
class ArtGalleryArtworkTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Artwork = cls.env['art.gallery.artwork']
        cls.artist = cls.env['res.partner'].create({
            'name': 'Test Artist',
            'is_artist': True,
        })

    def _create_artwork(self, **vals):
        return self.Artwork.create({'name': 'Test Artwork', **vals})

    # Constraints

    @mute_logger('odoo.sql_db')
    def test_negative_price(self):
        """The price cannot be negative."""
        with self.assertRaises(IntegrityError):
            self._create_artwork(price=-1)
            self.env.flush_all()

    def test_future_year(self):
        """The year cannot be in the future."""
        with self.assertRaises(ValidationError):
            self._create_artwork(year=fields.Date.today().year + 1)

    def test_current_year(self):
        """An artwork from the current year is accepted."""
        artwork = self._create_artwork(year=fields.Date.today().year)
        self.assertEqual(artwork.age, 0)

    @mute_logger('odoo.sql_db')
    def test_commission_above_100(self):
        """The commission cannot be above 100%."""
        with self.assertRaises(IntegrityError):
            self._create_artwork(commission_rate=150)
            self.env.flush_all()

    @mute_logger('odoo.sql_db')
    def test_negative_commission(self):
        """The commission cannot be negative."""
        with self.assertRaises(IntegrityError):
            self._create_artwork(commission_rate=-5)
            self.env.flush_all()

    @mute_logger('odoo.sql_db')
    def test_same_title_same_artist(self):
        """An artist cannot have 2 artworks with the same title."""
        self._create_artwork(artist_id=self.artist.id)
        with self.assertRaises(IntegrityError):
            self._create_artwork(artist_id=self.artist.id)
            self.env.flush_all()

    def test_same_title_other_artist(self):
        """2 artists can each have an artwork with the same title."""
        other_artist = self.env['res.partner'].create({'name': 'Other Artist', 'is_artist': True})
        self._create_artwork(artist_id=self.artist.id)
        self._create_artwork(artist_id=other_artist.id)
        self.env.flush_all()

    # Computed fields

    def test_age(self):
        """The age is computed from the year."""
        artwork = self._create_artwork(year=1888)
        self.assertEqual(artwork.age, fields.Date.today().year - 1888)

    def test_age_without_year(self):
        """Without a year, the age is 0."""
        self.assertEqual(self._create_artwork().age, 0)

    def test_artist_payout(self):
        """The artist gets the price minus the gallery commission."""
        artwork = self._create_artwork(price=1000, commission_rate=30)
        self.assertEqual(artwork.artist_payout, 700)
        artwork.commission_rate = 0
        self.assertEqual(artwork.artist_payout, 1000)

    # Artist

    def test_artist_artworks(self):
        """The artworks of an artist are listed on the artist."""
        artwork = self._create_artwork(artist_id=self.artist.id)
        self.assertEqual(self.artist.artwork_ids, artwork)
