from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestEstateProperty(TransactionCase):

    def setUp(self):
        super().setUp()
        
        self.property = self.env["estate.property"].create({
            "name": "Test Property",
            "expected_price": 5000
        })
        self.partner = self.env["res.partner"].create({"name": "Test Buyer"})
    
    def test_cannot_create_offer_for_sold_property(self):
        self.property.write({"state": "sold"})
        
        with self.assertRaises(UserError, msg="A sold property cannot receive offers"):
            self.env["estate.property.offer"].create({
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 5001
            })
    
    def test_cannot_sell_property_without_offer_accepted(self):
        with self.assertRaises(UserError, msg="Cannot sold properties with no offers"):
            self.property.action_mark_property_sold()

    def test_correctly_mark_property_sold(self):
        self.env["estate.property.offer"].create({
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 5001
        }).action_accept_offer()
        self.property.action_mark_property_sold()
        self.assertEqual(self.property.state, "sold", msg="Property not marked sold")        
