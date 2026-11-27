from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class ArtGalleryExhibitionTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Exhibition = cls.env['art.gallery.exhibition']
        cls.artwork = cls.env['art.gallery.artwork'].create({'name': 'Test Artwork'})
        cls.other_artwork = cls.env['art.gallery.artwork'].create({'name': 'Other Artwork'})
        cls.exhibition = cls.Exhibition.create({
            'name': 'Test Exhibition',
            'start_date': '1970-01-10',
            'end_date': '1970-02-10',
            'artwork_ids': [(4, cls.artwork.id)],
        })

    def _create_exhibition(self, start_date, end_date, artworks):
        return self.Exhibition.create({
            'name': 'Other Exhibition',
            'start_date': start_date,
            'end_date': end_date,
            'artwork_ids': [(6, 0, artworks.ids)],
        })

    # Dates

    def test_end_date_before_start_date(self):
        """End date should be after start date"""
        with self.assertRaises(ValidationError):
            self.exhibition.end_date = '1969-01-01'

    def test_is_finished(self):
        """An exhibition is finished once its end date is past."""
        self.assertTrue(self.exhibition.is_finished)
        today = fields.Date.today()
        current = self._create_exhibition(today, today, self.other_artwork)
        self.assertFalse(current.is_finished)

    # Overlapping exhibitions

    def test_overlap_same_artwork(self):
        """An artwork cannot be in 2 exhibitions on overlapping dates."""
        with self.assertRaises(ValidationError):
            self._create_exhibition('1970-02-01', '1970-03-01', self.artwork)

    def test_overlap_on_last_day(self):
        """Sharing a single day is already an overlap."""
        with self.assertRaises(ValidationError):
            self._create_exhibition('1970-02-10', '1970-03-01', self.artwork)

    def test_overlap_other_artwork(self):
        """Overlapping exhibitions are fine if they share no artwork."""
        self._create_exhibition('1970-02-01', '1970-03-01', self.other_artwork)

    def test_no_overlap_same_artwork(self):
        """An artwork can be in 2 exhibitions one after the other."""
        self._create_exhibition('1970-02-11', '1970-03-01', self.artwork)

    def test_move_dates_into_overlap(self):
        """Changing the dates cannot create an overlap."""
        other = self._create_exhibition('1970-03-01', '1970-04-01', self.artwork)
        with self.assertRaises(ValidationError):
            other.start_date = '1970-02-01'

    def test_overlap_added_from_artwork(self):
        """The overlap is also checked when adding the exhibition from the artwork."""
        other = self._create_exhibition('1970-02-01', '1970-03-01', self.other_artwork)
        with self.assertRaises(ValidationError):
            self.artwork.exhibition_ids = [(4, other.id)]

    def test_exhibitions_of_artwork(self):
        """The exhibitions of an artwork are listed on the artwork."""
        self.assertEqual(self.artwork.exhibition_ids, self.exhibition)
