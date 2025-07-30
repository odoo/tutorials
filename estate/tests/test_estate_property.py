from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(self):
        super(EstateTestCase, self).setUpClass()

        self.property = self.env['estate.property'].create({
            "name": "Test Property",
            "description": "A beautiful house in the city.",
            "postcode": "12345",
            "expected_price": 150000,
            "bedrooms": 3,
            "living_area": 120,
            "facades": 2,
            "garage": True,
            "garden": True,
            "garden_area": 50,
            "garden_orientation": "south",
            "active": True,
            "state": "new",
        })

        self.offer = self.env["estate.property.offer"].create({
            "price": 140000,
            "property_id": self.property.id,
            'partner_id': self.env.ref('base.res_partner_1').id,
        })

    def test_prevent_offer_on_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError, msg="You cannot create an offer for a sold property."):
            self.env["estate.property.offer"].create({
                "price": 135000,
                "property_id": self.property.id,
                'partner_id': self.env.ref('base.res_partner_1').id,
            })

    def test_prevent_selling_without_accepted_offer(self):
        with self.assertRaises(UserError, msg="You cannot sell a property with no accepted offers."):
            self.property.action_property_sold()

    def test_selling_a_valid_property(self):
        self.offer.status = 'accepted'  
        self.property.action_property_sold()
        self.assertEqual(self.property.state, 'sold', "Property should be marked as sold after selling it.")

