from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestRealEstateProperty(TransactionCase):

    def setUp(self):
        super().setUp()

        # Create a property type
        self.property_type = self.env["estate.property.type"].create({"name": "Apartment"})

        # Create a buyer
        self.buyer = self.env["res.partner"].create({"name": "John Doe"})

        # Create a property
        self.property = self.env["estate.property"].create({
            "name": "Modern Villa",
            "expected_price": 500000.0,
            "property_type": self.property_type.id
        })

        # Create an offer for the property
        self.offer = self.env["estate.property.offer"].create({
            "property_id": self.property.id,
            "price": 510000.0,
            "status": "accepted",
            "partner_id": self.buyer.id
        })

    def test_cannot_create_offer_for_sold_property(self):
        """Ensure a sold property cannot receive offers."""
        self.property.selling_price = 510000.0
        self.property.buyer_id = self.buyer
        self.property.action_sold()

        with self.assertRaises(UserError, msg="A sold property cannot receive offers!"):
            self.env["estate.property.offer"].create({
                "property_id": self.property.id,
                "price": 520000.0,
                "partner_id": self.buyer.id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        """Ensure a property cannot be sold without an accepted offer."""
        # Remove the accepted offer
        self.property.offer_ids.unlink()

        with self.assertRaises(UserError, msg="You cannot sell a property without an accepted offer."):
            self.property.action_sold()

    def test_property_marked_as_sold_correctly(self):
        """Ensure that selling a property correctly updates its state to 'sold'."""
        self.property.selling_price = 510000.0
        self.property.buyer_id = self.buyer
        self.property.action_sold()

        self.assertEqual(self.property.state, "sold", "Property should be marked as sold.")

    def test_garden_reset_on_uncheck(self):
        """Ensure that unchecking the garden checkbox resets garden area and orientation."""
        self.property.garden = True
        self.property._onchange_garden()
        self.assertEqual(self.property.garden_area, 10, "Garden area should be set to 10 when garden is checked.")
        self.assertEqual(self.property.garden_orientation, "north", "Garden orientation should default to North.")

        self.property.garden = False  # Disable the garden
        self.property._onchange_garden()
        self.assertEqual(self.property.garden_area, 0, "Garden area should reset to 0 when garden is unchecked.")
        self.assertFalse(self.property.garden_orientation, "Garden orientation should reset when garden is unchecked.")

