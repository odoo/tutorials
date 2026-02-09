from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buyer = cls.env["res.partner"].create({"name": "Test Buyer"})
        cls.test_property = cls.env["estate.property"].create(
            {
                "name": "Test House",
                "expected_price": 1000,
            }
        )

    def test_initial_state(self):
        self.assertEqual(self.test_property.state, "new")

    def test_create_offer(self):
        self.env["estate.property.offer"].create(
            {
                "price": 900,
                "partner_id": self.buyer.id,
                "property_id": self.test_property.id,
            }
        )

    def test_sold_property(self):
        property = self.env["estate.property"].create(
            {
                "name": "test1",
                "expected_price": 1000,
                "selling_price": 900,
            }
        )
        with self.assertRaises(UserError, msg="Customer not found"):
            property.action_sold()
