from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.estate.tests.common import TestEstateCommon


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class TestEstatePropertyOffer(TestEstateCommon):
    def test_create(self):
        """Test that an offer cannot be created for a sold property."""

        # Sell the property, so we have a sold property to create a new offer on
        self._sell_cozy_cottage()

        self.assertRecordValues(self.cozy_cottage,
            [{'name': "Cozy Cottage", 'state': 'sold'}])

        with self.assertRaises(UserError, msg="Cannot create an offer for a sold property"):
            self.env['estate.property.offer'].create([
                {
                    'price': 270000,
                    'partner_id': self.partner.id,
                    'property_id': self.cozy_cottage.id,
                }])
