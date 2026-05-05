from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged, Form


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_mark_as_sold_without_offer(self):
        self.property = self.env['estate.property'].create({
            'name': 'property1',
            'expected_price': 100,
            'state': 'offer'
        })
        with self.assertRaises(UserError):
            self.property.action_state_to_sold()

    def test_reset_garden(self):
        self.property = self.env['estate.property'].create({
            'name': 'property',
            'expected_price': 100,
            'garden': True,
            'garden_area': 20,
            'garden_orientation': 'north'
        })
        with Form(self.property) as f1:
            f1.garden = False
        self.assertFalse(self.property.garden, 'the garden should not be there anymore')
        self.assertEqual(self.property.garden_area, 0, "garden area should be reset")
        self.assertFalse(self.property.garden_orientation, "garden orientation is expected to be unset")
