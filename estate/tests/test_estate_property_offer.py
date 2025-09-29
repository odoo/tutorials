from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import TestEstateCommon


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class TestEstatePropertyOffer(TestEstateCommon):
    def test_create(self):
        """Test that an offer cannot be created for a sold property."""

        # Accept one offer to be able to sell the property
        self.offers[0].action_offer_accept()
        # Sell the property to create an offer on it
        self.properties[0].action_property_sold()

        self.assertRecordValues(self.properties, [
           {'name': "Cozy Cottage", 'state': 'sold'},
           {'name': "Modern Apartment", 'state': 'offer_received'},
           {'name': "Beachfront Villa", 'state': 'new'},
        ])

        with self.assertRaises(UserError, msg="Cannot create an offer for a sold property"):
            self.env['estate.property.offer'].create([
                {
                    'price': 270000,
                    'partner_id': self.partner.id,
                    'property_id': self.properties[0].id,  # Cozy Cottage
                }])
