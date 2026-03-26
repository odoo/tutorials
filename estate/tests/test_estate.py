from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Test Villa',
                'expected_price': 15,
                'postcode': '12345',
                'bedrooms': 3,
            }
        ])

        cls.offers = cls.env['estate.property.offer'].create([
            {
                'partner_id': cls.env.ref('base.main_partner').id,
                'property_id': cls.properties.id,
                'price': 14,
            }
        ])

    def test_offer_sold_property(self):
        self.offers.action_accept_offer()

        self.properties.action_change_state_to_sold()
        
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'partner_id': self.env.ref('base.main_partner').id,
                'property_id': self.properties.id,
                'price': 15,
            })
    
    def test_sell_with_no_accept(self):
        with self.assertRaises(UserError):
            self.properties.action_change_state_to_sold()
    
    def test_property_state(self):
        self.offers.action_accept_offer()

        self.properties.action_change_state_to_sold()

        self.assertEqual(self.properties.state, 'sold')
