from odoo.exceptions import UserError
from odoo.tests.common import tagged

from .common import TestCommon


@tagged("post_install", "-at_install")
class TestOfferForSoldProperty(TestCommon):
    def test_cant_create_offer_for_sold_property(self):
        offer = self.env["estate.property.offer"].create(
            {
                "price": 95000.0,
                "partner_id": self.buyer.id,
                "property_id": self.property.id,
            },
        )
        offer.action_accept()
        self.property.action_sold()
        self.assertEqual(self.property.state, "sold")

        with self.assertRaises(
            UserError, msg="Can't create offer for sold, accepted or canceled property.",
        ):
            self.env["estate.property.offer"].create(
                {
                    "price": 100000.0,
                    "partner_id": self.buyer.id,
                    "property_id": self.property.id,
                },
            )
