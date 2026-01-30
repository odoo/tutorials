from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "test property",
                    "expected_price": 100_000,
                }
            ]
        )

        cls.partners = cls.env["res.partner"].create(
            [
                {
                    "name": "test partner",
                }
            ]
        )

    def test_make_offer_for_new_property(self):
        """The property state should be 'offer_received' after receiving a property"""
        self._make_offer_on_property()

        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "test property",
                    "expected_price": 100_000,
                    "state": "offer_received",
                }
            ],
        )

    def test_sell_property_without_offer(self):
        """ "It should be impossible to sell a property that received no offer"""

        with self.assertRaises(UserError, msg="Properties without offers cannot be sold"):
            self.properties.action_sell()

    def test_sell_property_with_offer(self):
        """The property state should be 'sold' after selling the property"""
        self._make_offer_on_property()
        self.properties.action_sell()

        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "test property",
                    "state": "sold",
                }
            ],
        )

    def test_make_offer_for_sold_property(self):
        """ "It should be impossible to create an offer for a sold property"""
        self._make_offer_on_property()
        self.properties.action_sell()

        with self.assertRaises(UserError, msg="Sold properties cannot receive offers"):
            self.properties.offer_ids.create(
                [
                    {
                        "price": 300_000,
                        "property_id": self.properties.id,
                        "partner_id": self.partners.id,
                    }
                ]
            )

    def _make_offer_on_property(self):
        self.properties.offer_ids.create(
            [
                {
                    "price": 200_000,
                    "property_id": self.properties.id,
                    "partner_id": self.partners.id,
                }
            ]
        )
