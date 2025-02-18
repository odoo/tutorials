from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        partner = cls.env["res.partner"].create({"name": "Test Buyer"})

        cls.property = cls.env["estate.property"].create(
            [
                {
                    "name": "Property p1",
                    "expected_price": 1500,
                    "state": "new",
                    "buyer_id": partner.id,
                }
            ]
        )
        cls.property_offer = cls.env["estate.property.offer"].create(
            {
                "price": 1530,
                "partner_id": partner.id,
                "property_id": cls.property.id,
            }
        )

    def test_create_offer_on_sold_property(self):
        """Test that an offer cannot be created on a sold property."""
        self.property_offer.action_accept_offer()
        partner = self.env["res.partner"].create({"name": "Deco Addict"})

        self.property.action_set_sold()

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 1600,
                    "validity": 14,
                    "partner_id": partner.id,
                    "property_id": self.property.id,
                }
            )

    def test_sell_property_with_offer(self):
        """Test that a property cannot be sold without an accepted offer, and can be sold after the offer is accepted."""
        partner = self.env["res.partner"].create({"name": "Azur"})

        offer = self.env["estate.property.offer"].create(
            {
                "price": 1600,
                "property_id": self.property.id,
                "partner_id": partner.id,
            }
        )

        # Test: Property cannot be sold without an accepted offer
        with self.assertRaises(UserError):
            self.property.action_set_sold()

        # Accept the offer and sell the property
        offer.status = "accepted"
        self.property.action_set_sold()

        # Assert the property state is 'sold'
        self.assertEqual(self.property.state, "sold")

    def test_garden_field_behavior(self):
        """Test the behavior of garden-related fields when the garden checkbox is toggled."""
        with Form(self.property) as property:
            # Test when garden checkbox is unchecked
            property.garden = False
            self.assertEqual(property.garden_orientation, False)
            self.assertEqual(property.garden_area, 0)

            # Test when garden checkbox is checked
            property.garden = True
            self.assertEqual(property.garden_orientation, "north")
            self.assertEqual(property.garden_area, 20)
