from odoo.exceptions import UserError

from .common import EstateTestCommon


class TestEstatePropertyOffer(EstateTestCommon):
    def test_no_offer_can_be_created_for_sold_property(self):
        self.property_a.offer_ids[0].action_accept()
        self.property_a.action_mark_sold()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": self.property_a.best_price + 100.00,
                    "partner_id": self.env.user.partner_id.id,
                    "property_id": self.property_a.id,
                },
            )
