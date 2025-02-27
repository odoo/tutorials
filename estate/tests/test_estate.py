from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.buyer = cls.env["res.partner"].create({"name": "buyer", "email": "email@test.com"})

    def test_sold_property(self):
        property1 = self.env["estate.property"].create({"name" : "property1", "status": "new", "expected_price": 100})
        with self.assertRaises(UserError):
            property1.sold_property()
        offer = self.env["estate.property.offer"].create({"price": 100, "property_id": property1.id, "partner_id": self.buyer.id})
        offer.accept_offer()
        property1.sold_property()
        self.assertEqual(property1.status, "sold")

    def test_offer_creation(self):
        property2 = self.env["estate.property"].create({"name": "property2", "expected_price": 100, "status": "sold"})
        with self.assertRaises(UserError):
            offer = self.env["estate.property.offer"].create({"price": 100, "property_id": property2.id, "partner_id": self.buyer.id})