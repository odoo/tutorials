from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class EstatePropertyTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def test_offer_creation_on_sold_property(self):
        property = self.env["estate.property"].create(
            {
                "name": "Test case Property",
                "expected_price": "123",
            }
        )

        self.env["estate.property.offer"].create(
            {
                "price": 1500.00,
                "partner_id": self.env.ref("base.res_partner_1").id,
                "date_deadline": "2025-09-14",
                "property_id": property.id,
                "status": "accepted",
            }
        )

        property.sold_button_action()

        with self.assertRaises(
            UserError, msg="Cannot create an offer for a sold property"
        ):
            self.env["estate.property.offer"].create(
                {
                    "price": 1500.00,
                    "partner_id": self.env.ref("base.res_partner_1").id,
                    "date_deadline": "2025-09-14",
                    "property_id": property.id,
                }
            )

    def test_sell_property_on_accepted_offer(self):
        property = self.env["estate.property"].create(
            {
                "name": "Test case Property 2",
                "expected_price": "456",
            }
        )

        self.env["estate.property.offer"].create(
            {
                "price": 1500.00,
                "partner_id": self.env.ref("base.res_partner_1").id,
                "date_deadline": "2025-09-14",
                "property_id": property.id,
            }
        )
        with self.assertRaises(UserError):
            property.sold_button_action()
