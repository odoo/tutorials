from psycopg2 import IntegrityError

from odoo import Command
from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import Common


@tagged("post_install", "-at_install")
class TestAddCustomDutyLine(Common):
    
    @mute_logger("odoo.sql_db")
    def test_zero_or_positive_custom_duty_with_added_charges_constraint(self):
        duty_lines = self.custom_duty_wizard.account_move_custom_duty_line_ids
        
        self.assertTrue(duty_lines, "Custom duty lines are not added or linked with the wizard.")
        
        with self.assertRaises(IntegrityError, msg="Custom duty with added charges must be either 0 or positive."):
            duty_lines[0].write({ "custom_duty_with_added_charges": -123 })
    
    def test_compute_methods(self):
        """ Test computation of assessable value, taxable amount, and tax amount for duty lines. """
        duty_lines = self.custom_duty_wizard.account_move_custom_duty_line_ids
        
        self.assertTrue(len(duty_lines) >= 2, "Duty lines are not added or linked to the wizard.")
        
        custom_duty_for_line_0 = 750
        custom_duty_for_line_1 = 1200
        
        expected_assessable_value_for_line_0 = duty_lines[0].account_move_line_id.price_subtotal * duty_lines[0].account_move_custom_duty_id.custom_currency_rate
        expected_assessable_value_for_line_1 = duty_lines[1].account_move_line_id.price_subtotal * duty_lines[1].account_move_custom_duty_id.custom_currency_rate
        
        expected_taxable_amount_for_line_0 = custom_duty_for_line_0 + expected_assessable_value_for_line_0
        expected_taxable_amount_for_line_1 = custom_duty_for_line_1 + expected_assessable_value_for_line_1
                
        duty_lines[0].write({
            "tax_ids": [Command.link(self.igst_tax_5.id)],
            "custom_duty_with_added_charges": custom_duty_for_line_0
        })
        
        duty_lines[1].write({
            "tax_ids": [Command.link(self.igst_tax_5.id), Command.link(self.igst_tax_12.id)],
            "custom_duty_with_added_charges": custom_duty_for_line_1
        })
        
        expected_tax_amount_for_line_0 = round(expected_taxable_amount_for_line_0 * (5 / 100), 2)
        expected_tax_amount_for_line_1 = round(expected_taxable_amount_for_line_1 * ((5 + 12) / 100), 2)
        
        self.assertEqual(duty_lines[0].assessable_value, expected_assessable_value_for_line_0)
        self.assertEqual(duty_lines[1].assessable_value, expected_assessable_value_for_line_1)
        self.assertEqual(duty_lines[0].taxable_amount, expected_taxable_amount_for_line_0)
        self.assertEqual(duty_lines[1].taxable_amount, expected_taxable_amount_for_line_1)
        self.assertEqual(duty_lines[0].tax_amount, expected_tax_amount_for_line_0)
        self.assertEqual(duty_lines[1].tax_amount, expected_tax_amount_for_line_1)
