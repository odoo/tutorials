from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEstateOfferRules(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Client"})
        self.property = self.env["estate.property"].create(
            {
                "name": "Test House",
                "expected_price": 500000,
            }
        )

    def test_cannot_create_offer_on_sold_property(self):
        """Should raise UserError when trying to create an offer on sold property"""
        self.property.write({"state": "sold"})

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.partner.id,
                    "property_id": self.property.id,
                    "price": 400000,
                }
            )

    def test_cannot_sell_without_accepted_offer(self):
        """Should raise UserError if no accepted offer exists before selling"""
        # Add an offer but not accept it
        self.env["estate.property.offer"].create(
            {
                "partner_id": self.partner.id,
                "property_id": self.property.id,
                "price": 450000,
            }
        )

        with self.assertRaises(UserError):
            self.property.action_mark_sold()

    def test_successful_property_sale_with_accepted_offer(self):
        """Property should be sold when an accepted offer exists"""
        offer = self.env["estate.property.offer"].create(
            {
                "partner_id": self.partner.id,
                "property_id": self.property.id,
                "price": 550000,
            }
        )

        offer.action_accept_offer()

        self.property.action_mark_sold()
        self.assertEqual(self.property.state, "sold")
