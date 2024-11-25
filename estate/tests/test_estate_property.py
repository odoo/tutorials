from .common import TestEstateCommon

from odoo.tests import Form
from odoo.exceptions import UserError
from odoo.tests import tagged

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged("post_install", "-at_install")
class TestEstateProperty(TestEstateCommon):

    def test_compute_total_area(self):
        """Test that the total_area is computed like it should."""
        self.property.living_area = 20
        self.assertRecordValues(
            self.property,
            [
                {"total_area": 20},
            ]
        )

    def test_action_set_sold_StateSold(self):
        self.property.action_set_sold()
        self.assertRecordValues(
            self.property,
            [
                {"state": "sold"},
            ]
        )

    def test_action_set_cancelled_StateSold_UserError(self):
        """Test that everything behaves like it should when selling a property."""
        self.property.action_set_sold()

        with self.assertRaises(UserError):
            self.property.action_set_cancelled()

    def test_graden_onchange(self):
        property_form = Form(self.env["estate.property"].with_context(active_id=self.property.id))
        property_form.garden = True

        self.assertEqual(
            property_form.total_area, 10
        )
