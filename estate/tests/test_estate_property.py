from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class PropertyTest(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create([{
            'name': 'Big Villa',
            'state': 'sold',
            'description': 'A nice and big villa',
            'postcode': 12345,
            'date_availability': '2024-04-04',
            'expected_price': 1600000,
            'bedrooms': 6,
            'living_area': 100,
            'facades': 4,
            'garage': True,
            'garden': True,
            'garden_area': 100000,
            'garden_orientation': 'south',
        }, {
            'name': 'Cozy Cabin',
            'state': 'new',
            'description': 'Small cabin by lake',
            'postcode': 10000,
            'date_availability': '2024-04-04',
            'expected_price': 80000,
            'bedrooms': 2,
            'living_area': 10,
            'facades': 4,
            'garage': False,
            'garden': True,
            'garden_area': 100000,
            'garden_orientation': 'south',
        }])

    def test_property_sell_with_no_accepted_offer(self):
        with self.assertRaises(UserError):
            self.properties[1].action_set_sold()

    def test_offer_create_on_sold_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.properties[0].id,
                'partner_id': self.env.ref('base.res_partner_12').id,
                'price': 1600000
            })
