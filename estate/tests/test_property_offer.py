from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestPropertyOfferRules(TransactionCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.property = self.env["estate.property"].create(
            {
                "name": "Test Villa",
                "expected_price": 200000,
                "state": "new",
            }
        )
        self.partner = self.env["res.partner"].create({"name": "Test Buyer"})

    def test_cannot_create_offer_on_sold_property(self):
        self.property.state = "sold"
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 180000,
                    "partner_id": self.partner.id,
                    "property_id": self.property.id,
                }
            )

    def test_cannot_sell_without_accepted_offer(self):
        self.env["estate.property.offer"].create(
            {
                "price": 180000,
                "partner_id": self.partner.id,
                "property_id": self.property.id,
            }
        )
        with self.assertRaises(UserError):
            self.property.set_sold_state()

    def test_can_sell_with_accepted_offer(self):
        self.env["estate.property.offer"].create(
            {
                "price": 190000,
                "partner_id": self.partner.id,
                "property_id": self.property.id,
                "status": "accepted",
            }
        )
        self.property.set_sold_state()
        self.assertEqual(self.property.state, "sold")
