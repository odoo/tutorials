from odoo.tests.common import TransactionCase
from odoo.tests import Form
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Property = cls.env['estate.property']

    def test_create_an_offer_for_sold_property(self):
        prop = self.Property.create({
            'name': 'Test Property',
            'expected_price': 100000,
            'living_area': 100,
        })

        offer = self.env['estate.property.offer'].create({
            'price': 110000,
            'partner_id': self.env['res.partner'].create({'name': 'Test Partner'}).id,
            'property_id': prop.id,
        })

        offer.accept_offer()
        prop.action_set_sold()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 120000,
                'partner_id': self.env['res.partner'].create({'name': 'Another Partner'}).id,
                'property_id': prop.id,
            })

    def test_sell_property_without_accepted_offer(self):
        prop = self.Property.create({
            'name': 'Test Property 2',
            'expected_price': 150000,
            'living_area': 150,
        })

        with self.assertRaises(UserError):
            prop.action_set_sold()

    def test_garden_onchange_reset(self):
        with Form(self.env['estate.property']) as property_form:
            # Fill in the required fields to be safe (keep the form valid, respect the constraints)
            property_form.name = "Test Garden Property"
            property_form.expected_price = 200000
            property_form.living_area = 120

            property_form.garden = True

            property_form.garden_area = 50
            property_form.garden_orientation = 'south'
            self.assertEqual(property_form.garden_area, 50)
            self.assertEqual(property_form.garden_orientation, 'south')

            property_form.garden = False
            self.assertEqual(property_form.garden_area, 0)
            self.assertFalse(property_form.garden_orientation)
