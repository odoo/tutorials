from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import Common


@tagged("post_install", "-at_install")
class TestAccountMove(Common):
    
    @mute_logger("odoo.sql_db")
    def test_positive_bill_of_entry_custom_currency_rate_constraint(self):
        with self.assertRaises(IntegrityError, msg="Custom currency rate for bill of entry must be strictly positive."):
            self.vendor_bill.write({ "bill_of_entry_custom_currency_rate": 0 })
        
        with self.assertRaises(IntegrityError, msg="Custom currency rate for bill of entry must be strictly positive."):
            self.vendor_bill.write({ "bill_of_entry_custom_currency_rate": -123 })
