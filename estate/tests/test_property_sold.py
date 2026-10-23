from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


class TestPropertySold(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.buyer_1 = cls.env["res.partner"].create({"name": "First Buyer"})
        cls.buyer_2 = cls.env["res.partner"].create({"name": "Late Buyer"})

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Huis Hogewinkelstraat 20",
                "bedrooms": 6,
                "expected_price": 730000,
                "postcode": "3053",
                "living_area": 210,
            }
        )

    def test_create_offer_when_sold(self):
        self.env["estate.property.offer"].create(
            {
                "price": 720000,
                "partner_id": self.buyer_1.id,
                "property_id": self.property.id,
                "status": "accepted",
            }
        )
        self.property.action_sell()

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 740000,
                    "partner_id": self.buyer_2.id,
                    "property_id": self.property.id,
                }
            )

    def test_sell_without_offers(self):
        with self.assertRaises(ValidationError):
            self.property.action_sell()

    def test_sell_without_accepted_offers(self):
        self.env["estate.property.offer"].create(
            {
                "price": 720000,
                "partner_id": self.buyer_1.id,
                "property_id": self.property.id,
                "status": "refused",
            }
        )

        with self.assertRaises(ValidationError):
            self.property.action_sell()

    def test_check_stage_sold_property(self):
        self.env["estate.property.offer"].create(
            {
                "price": 720000,
                "partner_id": self.buyer_1.id,
                "property_id": self.property.id,
                "status": "accepted",
            }
        )
        self.property.action_sell()

        self.assertRecordValues(self.property, [
            {'stage': "sold"}
        ])
