from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEstateProperty(TransactionCase):
    def setUp(self):
        super(TestEstateProperty, self).setUpClass()
        self.property = self.env['estate.property'].create({
            "name": "test",
            "expected_price": 100,
        })
        self.partner = self.env['res.partner'].create({
            "name":"test",
        })

    def test_not_create_offer_of_sold_property(self):
        """Don't create an offer for sold property"""
        self.property.status = "sold"
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.partner.id,
                'price': 150,
            })
    
    def test_not_sell_property_with_no_accepted_offer(self):
        """Don't sell property with no accepted offer"""
        with self.assertRaises(UserError):
            self.property.status = "sold"

    def test_selling_property_marked_as_sold_after_selling_it(self):
        """Check that selling a property that can be sold is correctly marked as sold after selling it."""
        self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.partner.id,
                'price': 150,
            })
        self.property.action_sold()
        self.assertEqual(self.property.status, "sold")