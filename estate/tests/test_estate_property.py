from odoo.tests.common import TransactionCase, tagged
from odoo.tests import Form
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 200,
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'north',
        })
        cls.offer = cls.env['estate.property.offer'].create({
            'price': 1200,
            'property_id': cls.property.id,
            'partner_id': cls.env.ref('base.res_partner_1').id
        })

    def test_sold_property_cannot_create_offers(self):
        self.property.state = 'sold'

        with self.assertRaises(UserError, msg=""):
            self.env['estate.property.offer'].create({
                'price': 50000,
                'partner_id': self.env.ref('base.res_partner_1').id,
                'property_id': self.property.id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError, msg="You cannot sell a property with no accepted offers."):
            self.property.action_set_sold_status()

    def test_selling_property_with_accepted_offer(self):
        self.offer.status = 'accepted'
        self.property.action_set_sold_status()
        self.assertEqual(self.property.state, 'sold', "Property state should be updated to 'sold'")

    def test_onchange_garden(self):
        form = Form(self.property)
        form.garden = False

        self.assertEqual(form.garden_area, 0, "Garden area should reset to 0.")
        self.assertEqual(form.garden_orientation, False, "Garden orientation should be cleared.")
