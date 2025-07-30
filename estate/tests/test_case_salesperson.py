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
        self.property.action_set_sold()

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
            self.property.action_set_sold()

    def test_property_marked_as_sold_correctly(self):
        """Ensure that selling a property correctly updates its state to 'sold'."""
        self.property.selling_price = 510000.0
        self.property.buyer_id = self.buyer
        self.property.action_set_sold()

        self.assertEqual(self.property.state, "sold", "Property should be marked as sold.")