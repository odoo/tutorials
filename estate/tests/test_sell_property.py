from odoo.addons.estate.tests.common import EstateTestCommon
from odoo.exceptions import UserError


class TestSellProperty(EstateTestCommon):

    def test_sell_property(self):
        with self.assertRaises(UserError):
            self.property_1.estate_sold()
