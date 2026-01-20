from odoo.tests.common import TransactionCase
from odoo.tests import Form, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env.ref('base.res_partner_1')
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'description': "A property created for testing purpose.",
            'postcode': 12345,
            'bedrooms': 2,
            'living_area': 10,
            'facades': 2,
            'expected_price': 100000,
            'garden': True,
            'garden_area': 15,
            'garden_orientation': 'east',
            'active': True,
            'state': 'new',
        })

    def test_create_offer_for_sold_property(self):
        self.property.state = 'sold'

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 100000,
                'validity': 7,
                'partner_id': self.partner.id,
            })

    def test_sell_property_with_no_accepted_offer(self):
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 200000,
            'validity': 7,
            'partner_id': self.partner.id,
        })

        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_marked_sold_after_selling_property(self):
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 200000,
            'validity': 7,
            'partner_id': self.partner.id,
        })

        offer[0].action_accept()
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')

    def test_garden_reset_on_uncheck(self):
        property_form = Form(self.property)
        property_form.garden = False
        property_form.save()

        self.assertEqual(self.property.garden_area, 0)
        self.assertFalse(self.property.garden_orientation)
