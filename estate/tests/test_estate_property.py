from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    def setUp(self):
        super(TestEstateProperty, self).setUp()
        self.property = self.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'state': 'new',
        })
        self.offer = self.env['estate.property.offer'].create({
            'price': 100000,
            'property_id': self.property.id,
            'partner_id': self.env.ref('base.res_partner_12').id
        })

    def test_cannot_create_offer_for_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError, msg="You cannot create an offer for a sold property."):
            self.env['estate.property.offer'].create({
                'price': 80000,
                'property_id': self.property.id,
                'partner_id': self.env.ref('base.res_partner_12').id
            })

    def test_cannot_sell_property_with_no_accepted_offers(self):
        with self.assertRaises(UserError, msg="You cannot sell a property with no accepted offers."):
            self.property.action_property_sold()

    def test_can_sell_property_with_accepted_offer(self):
        self.offer.status = 'accepted'
        self.property.action_property_sold()
        
        self.assertEqual(self.property.state, 'sold', "Property should be sold first.")

    def test_onchange_garden(self):
        form = Form(self.property)
        form.garden = False

        self.assertRaises(form.garden_area, 0, "Garden area should be reset to 0.")
        self.assertRaises(form.garden_orientation, '', "Garden orienatation should be cleared when garden is unchecked.")
