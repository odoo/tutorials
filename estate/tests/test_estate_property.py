from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner_id = cls.env['res.partner'].create({'name': 'Test Partner'})

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'postcode': '123456',
            'expected_price': 123,
            'buyer_id': cls.partner_id.id,
            'state': 'new'
        })

        cls.property_no_offer = cls.env['estate.property'].create({
            'name': 'No Offer Property',
            'postcode': '123456',
            'expected_price': 123,
            'buyer_id': cls.partner_id.id,
            'state': 'new'
        })

        cls.offer = cls.env['estate.property.offer'].create({
            'price': 500000,
            'property_id': cls.property.id,
            'status': 'accepted',
            'partner_id': cls.partner_id.id
        })

    def test_create_offer_for_sold_property(self):
        self.property.state = 'sold'
        self.offer.status = 'accepted'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 600000,
                'property_id': self.property.id,
                'status': 'accepted',
                'partner_id': self.partner_id.id
            })

    def test_sell_property_without_accepted_offer(self):
        self.property_no_offer.state = 'new'
        with self.assertRaises(UserError, msg="You cannot sell a property without accepted offers."):
            self.property_no_offer.action_sold()

    def test_successful_property_sale(self):
        self.property.state = 'offer_accepted'
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold', "Property should be marked as sold.")

    def test_reset_garden_fields(self):
        self.property.garden = True
        self.property.garden_area = 150.0
        self.property.garden_orientation = 'north'
        self.property.garden = False
        self.property._onchange_garden()
        self.assertEqual(self.property.garden_area, 0.0)
        self.assertFalse(self.property.garden_orientation)
