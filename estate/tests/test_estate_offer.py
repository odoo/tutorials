from odoo.addons.estate.tests.common import TestEstateCommon
from odoo.exceptions import UserError


class TestEstateOffer(TestEstateCommon):
    def test_create_offer_sold(self):
        self.property.state = "sold"

        with self.assertRaises(UserError):
            self.env["estate.offer"].create(
                {
                    "partner_id": self.env.user.id,
                    "property_id": self.property.id,
                }
            )
