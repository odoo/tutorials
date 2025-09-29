from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import EstateTestCommon


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestProperty(EstateTestCommon):
    def test_action_property_sold(self):
        """Test that everything behaves like it should when selling a property."""

        # Accept one offer to be able to sell the property
        self.offers[0].action_offer_accept()

        self.properties[0].action_property_sold()

        self.assertRecordValues(self.properties, [
           {'name': "Cozy Cottage", 'state': 'sold'},
           {'name': "Modern Apartment", 'state': 'offer_received'},
           {'name': "Beachfront Villa", 'state': 'new'},
        ])

        with self.assertRaises(UserError, msg="A property with no accepted offer cannot be sold"):
            self.properties[1].action_property_sold()
        with self.assertRaises(UserError, msg="A property with no offers cannot be sold."):
            self.properties[2].action_property_sold()
