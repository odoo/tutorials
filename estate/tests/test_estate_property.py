from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    def setUp(self):
        super().setUp()
        self.property = self.env['estate.property'].create({
            'name': "Larg villa",
            'expected_price': 10000
        })
        self.partner = self.env['res.partner'].create({
            'name': "Red Wood"
        })

    def test_create_offer_for_sold_property(self):
        self.property.write({
            'state': 'sold'
        })
        with self.assertRaises(UserError, msg="Can't receive offer for sold property"):
            self.env['estate.property.offer'].create({
                'price': 20000,
                'partner_id': self.partner.id,
                'property_id': self.property.id
            })

    def test_sell_not_accepted_offer_property(self):
        with self.assertRaises(UserError, msg="Can't sell property because there isn't any offer accepted!"):
            self.property.action_set_sold()

    def test_property_selling(self):
        offer = self.env['estate.property.offer'].create({
            'price': 20000,
            'partner_id': self.partner.id,
            'property_id': self.property.id
        })
        offer.action_accept()
        self.property.action_set_sold()
        self.assertEqual(self.property.state, 'sold', "Property state should be changed to sold!")

    def test_garden_checkbox_reset(self):
        with Form(self.property) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10, "Garden Area should be 10 when Garden checkbox is checked!")
            self.assertEqual(form.garden_orientation, "north", "Garden Orientation should be North when Garden checkbox is checked!")
            form.garden = False
            self.assertEqual(form.garden_area, 0, "Garden Area should be reset to 0 when Garden checkbox is unchecked!")
            self.assertEqual(form.garden_orientation, False, "Garden Orientation should be reset to False when Garden checkbox is unchecked!")
