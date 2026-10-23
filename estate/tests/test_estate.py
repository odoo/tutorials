from odoo.tests import Form, TransactionCase
from odoo.exceptions import UserError, ValidationError


class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Test Property 1",
                    "expected_price": 100000.0,
                    "state": "new",
                },
                {
                    "name": "Test Property 2",
                    "expected_price": 200000.0,
                    "state": "new",
                },
            ]
        )

    def test_offer_sold_property(self):
        for property in self.properties:
            property.state = "sold"
            with self.assertRaises(ValidationError):
                self.env["estate.property.offer"].create(
                    {
                        "price": 150000.0,
                        "partner_id": self.env.user.partner_id.id,
                        "property_id": property.id,
                    }
                )

    def test_sell_property_no_accepted_offer(self):
        for property in self.properties:
            with self.assertRaises(UserError):
                property.action_sold()

    def test_garden_form_reset(self):
        for property in self.properties:
            with Form(property) as property_form:
                property_form.garden = True
                property_form.garden_area = 25
                property_form.garden_orientation = "south"
                property_form.garden = False
                self.assertEqual(property_form.garden_area, 0)
                self.assertFalse(property_form.garden_orientation)
                property_form.garden = True
                self.assertEqual(property_form.garden_area, 10)
                self.assertEqual(property_form.garden_orientation, "north")
