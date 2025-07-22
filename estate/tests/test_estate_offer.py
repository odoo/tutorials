# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestOfferCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Buyer"})
        cls.salesperson = cls.env["res.users"].create(
            {"name": "Test Salesperson", "login": "test.salesperson@example.com"}
        )
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Test Property",
                "expected_price": 500000,
                "state": "new",
                "user_id": cls.salesperson.id,
            }
        )

    def test_cannot_create_offer_on_sold_property(self):
        """Prevent creating offers for sold property"""
        self.property.write({"state": "sold"})
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.partner.id,
                    "property_id": self.property.id,
                    "price": 510000,
                    "validity": 10,
                }
            )

    def test_cannot_sell_property_without_accepted_offer(self):
        """Prevent selling property with no accepted offer"""
        with self.assertRaises(ValidationError) as ctx:
            self.property.action_property_sold()
        self.assertIn(
            "Cannot mark as sold. No accepted offer found for this property.",
            str(ctx.exception),
        )

    def test_can_sell_property_with_accepted_offer(self):
        """Allow selling property if accepted offer exists"""
        offer = self.env["estate.property.offer"].create(
            {
                "partner_id": self.partner.id,
                "property_id": self.property.id,
                "price": 520000,
                "validity": 10,
            }
        )
        offer.action_accept()
        self.property.action_property_sold()
        self.assertEqual(self.property.state, "sold", "Property should be marked as sold.")
        self.assertEqual(self.property.buyer_id.id, self.partner.id, "Buyer should be set correctly.")
        self.assertEqual(self.property.selling_price, offer.price, "Selling price should match accepted offer price.")
        self.assertEqual(self.property.user_id.id, self.salesperson.id, "Salesman should be set correctly.")

    def test_reset_garden_fields_when_garden_unchecked(self):
        """Unchecking garden resets garden_area and garden_orientation"""
        property = self.env["estate.property"].create(
            {
                "name": "Test Villa",
                "expected_price": 500000,
                "garden": True,
                "garden_area": 500,
                "garden_orientation": "north",
            }
        )
        property.garden = False
        property._onchange_garden()
        self.assertEqual(property.garden_area, 0, "Garden area should reset to 0")
        self.assertFalse(
            property.garden_orientation, "Garden orientation should reset to False"
        )
