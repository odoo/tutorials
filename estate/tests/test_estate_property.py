from psycopg2 import errors

from odoo.exceptions import UserError
from odoo.tests import Form, tagged

from .common import TestCommon


@tagged("post_install", "-at_install")
class TestEstateProperty(TestCommon):
    def test_01_property_defaults(self):
        property_test = self.env["estate.property"].create(
            {
                "name": "Test House",
                "expected_price": 10000.0,
            },
        )
        self.assertEqual(property_test.state, "new")
        self.assertEqual(property_test.bedrooms, 2)
        self.assertTrue(property_test.active)

    def test_02_total_area(self):
        self.property.living_area = 100
        self.property.garden_area = 50
        self.assertEqual(self.property.total_area, 150)

    def test_03_garden_onchange(self):
        with Form(self.env["estate.property"].with_context(default_property_type_id=self.property_type.id)) as prop_form:
            prop_form.name = "Garden Test"
            prop_form.expected_price = 10000.0
            prop_form.garden = True
            self.assertEqual(prop_form.garden_area, 10)
            self.assertEqual(prop_form.garden_orientation, "north")

            prop_form.garden = False
            self.assertEqual(prop_form.garden_area, 0)
            self.assertFalse(prop_form.garden_orientation)

    def test_04_expected_price_constraint(self):
        """Test that expected price must be positive."""
        with self.assertRaises(errors.CheckViolation):
            self.env["estate.property"].create(
                {
                    "name": "Negative Price House",
                    "expected_price": -100.0,
                },
            )

    def test_05_selling_price_constraint(self):
        self.property.expected_price = 100000.0
        with self.assertRaises(
            UserError,
            msg="Selling price must be at least 90% of the expected price",
        ):
            self.property.selling_price = 80000.0
            self.property._constrains_selling_price()

    def test_06_action_cancel(self):
        self.property.action_cancel()
        self.assertEqual(self.property.state, "canceled")

        self.property.state = "sold"
        with self.assertRaises(UserError, msg="Sold properties cannot be canceled"):
            self.property.action_cancel()

    def test_07_action_sold(self):
        with self.assertRaises(UserError, msg="Property must have an accepted offer"):
            self.property.action_sold()

        offer = self.env["estate.property.offer"].create(
            {
                "price": 95000.0,
                "partner_id": self.buyer.id,
                "property_id": self.property.id,
            },
        )
        offer.action_accept()
        self.assertEqual(self.property.state, "offer_accepted")

        self.property.action_sold()
        self.assertEqual(self.property.state, "sold")
        self.assertEqual(self.property.selling_price, 95000.0)
        self.assertEqual(self.buyer.id, offer.partner_id.id)
        self.property.state = "canceled"
        with self.assertRaises(UserError, msg="Canceled properties cannot be sold"):
            self.property.action_sold()
