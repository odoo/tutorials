from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, tagged


@tagged("-at_install", "post_install")
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Sold Property",
                "expected_price": 100000,
                "living_area": 5,
                "garden": True,
                "garden_area": 20,
                "garden_orientation": "east",
                "postcode": 1233,
            }
        )

        cls.buyer = cls.env["res.partner"].create({"name": "Test Buyer"})

    def test_create_offer_on_sold_property(self):
        with self.assertRaises(ValidationError):
            self.property.state = "sold"
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.property.id,
                    "price": 110000,
                    "partner_id": self.buyer.id,
                }
            )

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_property_is_marked_sold_after_successful_sale(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "price": 120000,
                "partner_id": self.buyer.id,
            }
        )
        offer.action_set_accept_offer()
        self.property.action_set_sold()
        self.assertEqual(
            self.property.state,
            "sold",
            "Property should be marked as sold after selling",
        )

    def test_garden_uncheck(self):
        with Form(self.property) as property:
            self.assertTrue(property.garden)
            self.assertEqual(property.garden_area, 20)
            self.assertEqual(property.garden_orientation, "east")
            property.garden = False
            property.save()

        self.assertFalse(self.property.garden)
        self.assertEqual(self.property.garden_area, 0)
        self.assertFalse(self.property.garden_orientation)
