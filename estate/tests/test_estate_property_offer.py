from .common import TestEstateCommon

from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged("post_install", "-at_install")
class TestEstatePropertyOffer(TestEstateCommon):

    def test_action_create_PropertySold_UserError(self):

        self.property.action_set_sold()
        # create an offer
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                "property_id": self.property.id,
                "price": 2000,
                "partner_id": self.env.user.partner_id.id,
            })
