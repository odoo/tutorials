from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import Form, TransactionCase


@tagged("post_install", "-at_install")
class EstatePropertyTest(TransactionCase):
    """Test the estate property module business logic"""

    def setUp(self):
        """Set up data for each test method"""
        super().setUp()

        self.property_type = self.env["estate.property.type"].create(
            {
                "name": "Test Type",
            },
        )

        self.test_property = self.env["estate.property"].create(
            {
                "name": "Test Property",
                "expected_price": 100000,
                "living_area": 100,
                "property_type_id": self.property_type.id,
            },
        )

        self.partner1 = self.env.ref("base.res_partner_2")
        self.partner2 = self.env.ref("base.res_partner_12")

    def test_create_property_offer(self):
        """Test that creating offers changes property state and validates prices"""
        first_offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.test_property.id,
                "partner_id": self.partner1.id,
                "price": 90000,
            },
        )

        # Verify first offer was created and state changed
        self.assertEqual(self.test_property.state, "offer_received")
        self.assertEqual(first_offer.price, 90000)

        second_offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.test_property.id,
                "partner_id": self.partner2.id,
                "price": 110000,
            },
        )

        # Verify both offers exist and second offer is higher
        self.assertEqual(len(self.test_property.offer_ids), 2)
        self.assertGreater(second_offer.price, first_offer.price)
        self.assertEqual(self.test_property.best_price, 110000)

    def test_accept_offer_and_sell(self):
        """Test accepting an offer and selling a property"""
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.test_property.id,
                "partner_id": self.partner1.id,
                "price": 95000,
            },
        )

        offer.action_accept()

        self.assertEqual(self.test_property.state, "offer_accepted")
        self.assertEqual(offer.state, "accepted")

        self.test_property.action_sold()

        self.assertEqual(self.test_property.state, "sold")

        self.assertEqual(self.test_property.buyer_id, self.partner1)

        self.assertEqual(self.test_property.selling_price, 95000)

    def test_cancel_property(self):
        """Test property cancellation"""
        self.test_property.action_cancel()

        self.assertEqual(self.test_property.state, "canceled")

        with self.assertRaises(UserError, msg="Canceled properties cannot be sold"):
            self.test_property.action_sold()

    def test_property_constraints(self):
        """Test property validation constraints"""
        with self.assertRaises(Exception):
            self.env["estate.property"].create(
                {
                    "name": "Negative Price Property",
                    "expected_price": -10000,
                },
            )

        property_for_price_check = self.env["estate.property"].create(
            {
                "name": "Price Check Property",
                "expected_price": 100000,
                "living_area": 100,
            },
        )

        low_offer = self.env["estate.property.offer"].create(
            {
                "property_id": property_for_price_check.id,
                "partner_id": self.partner1.id,
                "price": 80000,
            },
        )

        with self.assertRaises(
            ValidationError,
            msg="The selling price must be at least 90% of the expected price",
        ):
            low_offer.action_accept()

    def test_multiple_offers(self):
        """Test that accepting an offer refuses other offers"""
        offer1 = self.env["estate.property.offer"].create(
            {
                "property_id": self.test_property.id,
                "partner_id": self.partner1.id,
                "price": 90000,
            },
        )

        offer2 = self.env["estate.property.offer"].create(
            {
                "property_id": self.test_property.id,
                "partner_id": self.partner2.id,
                "price": 100000,
            },
        )

        offer1.action_accept()

        with self.assertRaises(UserError, msg="An offer as already been accepted"):
            offer2.action_accept()

    def test_cannot_offer_on_sold_property(self):
        """Test cannot create offers for sold properties"""
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.test_property.id,
                "partner_id": self.partner1.id,
                "price": 95000,
            },
        )

        offer.action_accept()
        self.test_property.action_sold()

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.test_property.id,
                    "partner_id": self.partner2.id,
                    "price": 110000,
                },
            )

    def test_garden_onchange(self):
        """Test garden onchange functionality using Form"""
        with Form(self.test_property) as form:
            form.garden = True

            self.assertEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, "N")

            form.garden = False

            self.assertEqual(form.garden_area, 0)
            self.assertEqual(form.garden_orientation, False)

    def test_computed_total_area(self):
        """Test total area computation"""
        self.test_property.write(
            {
                "garden": True,
                "garden_area": 50,
                "living_area": 150,
            },
        )

        self.assertEqual(self.test_property.total_area, 200)
