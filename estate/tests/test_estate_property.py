from odoo.exceptions import UserError
from odoo.tests import Form, tagged

from odoo.addons.estate.tests.common import TestEstateCommon


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class TestEstateProperty(TestEstateCommon):
    def test_action_property_sold(self):
        """Test that everything behaves like it should when selling a property."""

        # Accept one offer to be able to sell the property
        self._sell_cozy_cottage()

        self.assertRecordValues(self.cozy_cottage,
           [{'name': "Cozy Cottage", 'state': 'sold'}])

        with self.assertRaises(UserError, msg="A property with no accepted offer cannot be sold"):
            self.modern_apartment.action_property_sold()
        with self.assertRaises(UserError, msg="A property with no offers cannot be sold."):
            self.beachfront_villa.action_property_sold()

    def test_onchange_garden(self):
        """Test that everything behaves as it should when unchecking garden"""

        self.assertRecordValues(self.cozy_cottage, [
           {'name': "Cozy Cottage", 'garden': True, 'garden_area': 20, 'garden_orientation': 'north'},
        ])

        # Use Form to trigger onchanges
        with Form(self.cozy_cottage) as f:
            f.garden = False

        self.assertRecordValues(self.cozy_cottage, [
           {'name': "Cozy Cottage", 'garden': False, 'garden_area': 0, 'garden_orientation': None},
        ])
