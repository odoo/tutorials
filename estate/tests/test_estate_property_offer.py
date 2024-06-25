from odoo.exceptions import UserError

from .test_estate_common import EstateCommonTest


class TestPropertyOffer(EstateCommonTest):
    def test_create_offer_on_sold_property(self):
        sold_property = self.env["estate.property"].create(
            {"expected_price": 100, "a_new_field_two": "Hello", "state": "sold"}
        )
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 100,
                    "property_id": sold_property.id,
                    "partner_id": self.partner.id,
                }
            )
