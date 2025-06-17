from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form


class EstatePropertyTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def test_offer_creation_on_sold_property(self):
        property = self.env["estate.property"].create(
            {
                "name": "Test case Property",
                "expected_price": "123",
            }
        )

        self.env["estate.property.offer"].create(
            {
                "price": 1500.00,
                "partner_id": self.env.ref("base.res_partner_1").id,
                "date_deadline": "2025-09-14",
                "property_id": property.id,
                "status": "accepted",
            }
        )

        property.action_sold()

        with self.assertRaises(
            UserError, msg="Cannot create an offer for a sold property"
        ):
            self.env["estate.property.offer"].create(
                {
                    "price": 1500.00,
                    "partner_id": self.env.ref("base.res_partner_1").id,
                    "date_deadline": "2025-09-14",
                    "property_id": property.id,
                }
            )

    def test_sell_property_on_accepted_offer(self):
        property = self.env["estate.property"].create(
            {
                "name": "Test case Property 2",
                "expected_price": "456",
            }
        )

        self.env["estate.property.offer"].create(
            {
                "price": 1500.00,
                "partner_id": self.env.ref("base.res_partner_1").id,
                "date_deadline": "2025-09-14",
                "property_id": property.id,
            }
        )
        with self.assertRaises(UserError) as cm:
            property.action_sold()
        self.assertEqual(
            cm.exception,
            "Offer must be accepted before selling the property.",
        )

    def test_reset_garden_area_and_orientation(self):
        property = self.env["estate.property"].create(
            {
                "name": "Garden Test Property",
                "expected_price": "789",
                "garden": True,
                "garden_area": 50,
                "garden_orientation": "north",
            }
        )

        with Form(property) as form:
            form.garden = False
            form.save()

        self.assertFalse(property.garden, "Garden checkbox should be unchecked.")
        self.assertFalse(
            property.garden_area,
            "Garden area should be reset when the garden checkbox is unchecked.",
        )
        self.assertFalse(
            property.garden_orientation,
            "Orientation should be reset when the garden checkbox is unchecked.",
        )
