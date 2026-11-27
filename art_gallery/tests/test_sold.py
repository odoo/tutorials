from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class ArtGalleryTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.artist = cls.env['res.partner'].create({
            'name': 'Test Artist',
            'is_artist': True,
        })
        cls.artwork = cls.env['art.gallery.artwork'].create({
            'name': 'Test Artwork',
            'artist_id': cls.artist.id,
            'price': 1000,
        })

    def test_new_artwork_is_available(self):
        """A new artwork is available by default."""
        self.assertEqual(self.artwork.status, 'available')

    def test_reserve_artwork(self):
        """Reserving an available artwork changes its status to reserved."""
        self.artwork.action_reserve()
        self.assertEqual(self.artwork.status, 'reserved')

    def test_sell_artwork(self):
        """Selling an artwork change the status to sold and make the price unchangeable"""
        self.artwork.action_sell()
        self.assertRecordValues(self.artwork, [{
            'status': 'sold',
        }])
        with self.assertRaises(UserError):
            self.artwork.price = 0

    def test_sell_reserved_artwork(self):
        """A reserved artwork can be sold."""
        self.artwork.action_reserve()
        self.artwork.action_sell()
        self.assertEqual(self.artwork.status, 'sold')

    def test_reserve_sold_artwork(self):
        """A sold artwork cannot be reserved."""
        self.artwork.action_sell()
        with self.assertRaises(UserError):
            self.artwork.action_reserve()

    def test_change_price_of_available_artwork(self):
        """The price of an artwork that is not sold can be changed."""
        self.artwork.price = 2000
        self.assertEqual(self.artwork.price, 2000)

    def test_edit_other_fields_of_sold_artwork(self):
        """Only the price is locked on a sold artwork."""
        self.artwork.action_sell()
        self.artwork.description = 'Sold at the spring auction'
        self.assertEqual(self.artwork.description, 'Sold at the spring auction')

    def test_delete_sold_artwork(self):
        """A sold artwork cannot be deleted."""
        self.artwork.action_sell()
        with self.assertRaises(UserError):
            self.artwork.unlink()

    def test_delete_available_artwork(self):
        """An artwork that is not sold can be deleted."""
        self.artwork.unlink()
        self.assertFalse(self.artwork.exists())

    def test_copy_sold_artwork(self):
        """A copy of a sold artwork is available again."""
        self.artwork.action_sell()
        copy = self.artwork.copy({'name': 'Test Artwork (copy)'})
        self.assertEqual(copy.status, 'available')
