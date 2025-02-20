from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestPropertySell(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.buyer_id = cls.env['res.partner'].create({'name': 'Temp Buyer'})

        cls.property= cls.env['estate.property'].create({
            'name': 'Temp Property',
            'description':'Temp prop',
            'postcode': '111',
            'expected_price': '100',
            'buyer_id': cls.buyer_id.id
        })

        cls.property_without_offer = cls.env['estate.property'].create({
            'name': 'Without Offer Property',
            'description':'Temp prop',
            'postcode': '222',
            'expected_price': '200',
            'buyer_id': cls.buyer_id.id
        })

        cls.offer = cls.env['estate.property.offer'].create({
            'price': 95,
            'property_id': cls.property.id,
            'status': 'accepted',
            'buyer_id': cls.buyer_id.id
        })


    def test_create_offer_for_sold_property(self):
        self.property.state = 'offer_accepted'
        self.property.property_action_sell()
        with self.assertRaises(UserError, msg="You cannot create an offer for a sold property."):
            self.env['estate.property.offer'].create({
                'price': 95,
                'property_id': self.property.id,
                'status': 'accepted',
                'buyer_id': self.buyer_id.id
            })

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError, msg="You cannot sell a property that hasn't any accepted offers."):
            self.property_without_offer.property_action_sell()

    def test_property_sold(self):
        self.property.state = 'offer_accepted'
        self.property.property_action_sell()
        self.assertEqual(self.property.state, 'sold',
            "Property should be marked as sold.")

    def test_onchange_garden_checkbox(self):
        with Form(self.property) as form:
            form.garden = True
            form.garden = False
            self.assertEqual(form.garden_area, 0,
                "Garden Area should be reset to 0 when Garden checkbox is unchecked")
            self.assertEqual(form.garden_orientation, False,
                "Garden Orientation should be reset to False when Garden checkbox is unchecked")
