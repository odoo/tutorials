from odoo.tests import Form, TransactionCase
from odoo.exceptions import UserError


class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.type = cls.env['estate.property.type'].create(
            {'name': 'Castle'}
        )
        cls.property = cls.env['estate.property'].create(
            {
                'name': 'test_property',
                'type_id': cls.type.id,
                'expected_price': 123.00,
                'state': 'received'
            }
        )
        cls.offer = cls.env['estate.property.offer'].create(
            {
                'price': 129.00,
                'property_id': cls.property.id,
            }
        )

    def test_action_sell(self):
        with self.assertRaises(UserError, msg='Cannot sell property with no accepted offers.'):
            self.property.action_set_state_sold()
        self.offer.state = 'accepted'
        self.property.action_set_state_sold()

    def test_offer_create(self):
        self.offer.state = 'accepted'
        self.property.action_set_state_sold()
        with self.assertRaises(UserError, msg='Cannot create an offer on an already sold property.'):
            self.env['estate.property.offer'].create({'price': '130', 'property_id': self.property.id})

    def test_garden_checkbox_onchange(self):
        f = Form(self.property)
        f.garden = True

        self.assertEqual(f.garden_area, 10)
        self.assertEqual(f.garden_orientation, 'north')

        f.garden = False

        self.assertEqual(f.garden_area, 0)
        self.assertFalse(f.garden_orientation)
