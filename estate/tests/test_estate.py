from odoo.tests import Form, TransactionCase
from odoo.exceptions import UserError


class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.a_buyer = cls.env["res.partner"].create({"name": "The Buyer"})
        cls.a_property_without_any_offers = cls.env["estate.property"].create(
            {"name": "The Property No One Wants", "expected_price": 1000000}
        )
        cls.a_property_with_an_offer = cls.env["estate.property"].create(
            {"name": "The Property", "expected_price": 100000}
        )
        cls.initial_offer = cls.env["estate.property.offer"].create(
            [
                {
                    "partner_id": cls.a_buyer.id,
                    "property_id": cls.a_property_with_an_offer.id,
                    "price": 101000,
                }
            ]
        )

    def test_property_without_any_offer_cannot_be_sold(self):
        """Test that a property without any offers cannot be sold."""
        with self.assertRaises(UserError):
            self.a_property_without_any_offers.action_sold()

    def test_property_without_any_accepted_offer_cannot_be_sold(self):
        """Test that a property without any accepted offers cannot be sold."""
        with self.assertRaises(UserError):
            self.a_property_with_an_offer.action_sold()

    def test_property_can_be_sold_if_one_offer_is_accepted(self):
        """Test that a property can be sold if one offer is accepted."""
        self.initial_offer.action_accept()
        self.a_property_with_an_offer.action_sold()
        self.assertRecordValues(
            self.a_property_with_an_offer,
            [
                {"state": "sold"},
            ],
        )

    def test_cannot_create_offer_if_property_is_sold(self):
        """Test that one cannot create an offer if the property is sold."""
        self.initial_offer.action_accept()
        self.a_property_with_an_offer.action_sold()
        with self.assertRaisesRegex(UserError, r"already been sold"):
            self.env["estate.property.offer"].create(
                [
                    {
                        "partner_id": self.a_buyer.id,
                        "property_id": self.a_property_with_an_offer.id,
                        "price": 200000,
                    }
                ]
            )

    def test_new_offer_bid_must_be_higher_than_previous_offer_bids(self):
        """Test that a new offer must be higher than the already existing ones"""
        with self.assertRaisesRegex(UserError, r"must be higher"):
            self.env["estate.property.offer"].create(
                [
                    {
                        "partner_id": self.a_buyer.id,
                        "property_id": self.a_property_with_an_offer.id,
                        "price": 1,
                    }
                ]
            )

    def test_garden_on_change(self):
        """Test the garden tick box behaviour:
        - ticking the checkbox sets the garden area = 10 and orientation to 'north'
        - unticking the checkbox sets the garden area = 0 and the orienation to false"""
        with Form(self.a_property_without_any_offers) as property_form:
            property_form.garden = True
            self.assertEqual(property_form.garden_area, 10)
            self.assertEqual(property_form.garden_orientation, "north")
            property_form.garden = False
            self.assertEqual(property_form.garden_area, 0)
            self.assertEqual(property_form.garden_orientation, False)
