from odoo.exceptions import UserError
from odoo.tests import tagged
from . import common


@tagged('post_install', '-at_install', 'estate_test')
class TestEstatePropretySold(common.TestEstatePropertyCommon):
    @classmethod
    def setUpClass(cls):
        super(TestEstatePropretySold, cls).setUpClass()

    def test_when_without_offers_should_raise_error(self):
        """Test that a property cannot be sold without any offers."""

        with self.assertRaises(UserError):
            self.property_1.action_sold()

    def test_when_sold_with_valid_should_update_state(self):
        self.property_3.action_sold()
        self.assertRecordValues(self.property_3, [{'state': 'sold'}])

    def test_when_status_cancelled_should_raise_error(self):
        with self.assertRaises(UserError):
            self.property_4.action_sold()
