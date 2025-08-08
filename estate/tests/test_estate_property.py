from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import Form


class TestestateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Sold Property",
                "expected_price": 100000,
                "garden": "False",
                "garden_area": 10,
                "garden_orientation": "north",
            }
        )

        cls.buyer = cls.env["res.partner"].create({"name": "Test Buyer"})

    def test_on_offer_sold_property(self):
        with self.assertRaises(ValidationError):
            self.property.state = "sold"
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.property.id,
                    "price": 110000,
                    "partner_id": self.buyer.id,
                }
            )

    def test_sell_property_without_offers(self):
        with self.assertRaises(ValidationError):
            self.property.action_set_sold_property()

    def test_property_is_successful_sold_after_sale(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "price": 120000,
                "partner_id": self.buyer.id,
            }
        )
        offer.action_accepted()
        self.property.action_set_sold_property()
        self.assertEqual(
            self.property.state,
            "sold",
            "Property should be marked as sold after selling",
        )

    def test_garden_uncheck(self):
        with Form(self.property) as property:
            self.assertTrue(property.garden)
            self.assertEqual(property.garden_area, 10)
            self.assertEqual(property.garden_orientation, "north")
            property.garden = False
            property.save()

        self.assertFalse(self.property.garden)
        self.assertEqual(self.property.garden_area, 0)
        self.assertFalse(self.property.garden_orientation)
