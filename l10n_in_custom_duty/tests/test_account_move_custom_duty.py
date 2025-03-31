from odoo import Command
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged

from .common import Common


@tagged("post_install", "-at_install")
class TestAddCustomDuty(Common):
    def test_default_get(self):
        self.assertEqual(self.custom_duty_wizard.import_duty_bill_id, self.vendor_bill, "Active bill should be set correctly.")        
        self.assertEqual(self.custom_duty_wizard.journal_id, self.company_india.import_custom_duty_journal_id, "Import custom duty journal must be set correctly.")
        self.assertEqual(self.custom_duty_wizard.journal_id, self.company_india.import_custom_duty_journal_id, "Import custom duty journal must be set correctly.")
        self.assertTrue(self.custom_duty_wizard.account_move_custom_duty_line_ids.mapped("account_move_line_id.id") <= self.vendor_bill.mapped("invoice_line_ids.id"), "Custom duty lines must be from linked vendor bill.")
        self.assertEqual(self.custom_duty_wizard.import_duty_bill_id, self.vendor_bill, "Reference bill should be set correctly.")
        self.assertFalse(self.custom_duty_wizard.bill_of_entry_id, "Bill of entry must not be there for fresh vendor bill.")
        self.assertFalse(self.custom_duty_wizard.line_ids, "Bill of entry lines must be not be there for fresh vendor bill.")
    
    def test_action_create_and_post_journal_entry_without_settings_configured(self):
        """ Ensure journal entry creation fails if required accounts are not configured in company settings. """
        self.company_india.import_custom_duty_account_id = False
        self.company_india.import_default_tax_account_id = False
        
        with self.assertRaises(UserError, msg="Custom Duty Account or Default Tax Account is not set in company settings."):
            self.custom_duty_wizard.action_create_and_post_journal_entry()   
    
    def test_action_create_and_post_journal_entry_with_settings_configured(self):
        """ Test journal entry creation, posting, and resetting with configured company settings. """
        duty_lines = self.custom_duty_wizard.account_move_custom_duty_line_ids
        
        self.assertTrue(duty_lines, "Custom duty lines are not added or linked with the wizard.")
        duty_lines[0].write({"tax_ids": [Command.link(self.igst_tax_5.id)]})
        duty_lines[1].write({"tax_ids": [Command.link(self.igst_tax_5.id), Command.link(self.igst_tax_12.id)]})
        
        self.assertFalse(self.vendor_bill.bill_of_entry_id, "Bill of Entry should not exist initially.")
        
        self.custom_duty_wizard.action_create_and_post_journal_entry()
        self.assertEqual(len(self.vendor_bill.bill_of_entry_id.line_ids), 5, "Journal line must be added properly.")
        self.assertTrue(self.vendor_bill.bill_of_entry_id, "Bill of Entry should be created and linked after calling the method.")
        self.assertEqual(self.vendor_bill.bill_of_entry_id.move_type, "entry", "Generated entry should be of type entry.")
        self.assertEqual(self.vendor_bill.bill_of_entry_id.state, "posted", "Generated entry should be in state posted.")
        
        self.custom_duty_wizard.bill_of_entry_id = self.vendor_bill.bill_of_entry_id
        self.custom_duty_wizard.action_reset_journal_to_draft()
        self.assertEqual(self.vendor_bill.bill_of_entry_id.state, "draft", "Bill of entry state must be reset to draft after calling the action.")
        
        bill_entry_id = self.vendor_bill.bill_of_entry_id.id

        self.custom_duty_wizard.action_create_and_post_journal_entry()
        self.assertEqual(self.vendor_bill.bill_of_entry_id.id, bill_entry_id, "Existing Bill of Entry should be updated, not replaced")
        self.assertEqual(self.vendor_bill.bill_of_entry_id.state, "posted", "Journal entry should be posted after method execution")
    
    def test_no_custom_line_constrains(self):
        self.assertTrue(self.custom_duty_wizard.account_move_custom_duty_line_ids, "Custom duty lines must be linked to the wizard.")
                
        with self.assertRaises(ValidationError, msg="Atleast one custom duty line must be added."):
            self.custom_duty_wizard.write({ "account_move_custom_duty_line_ids": [Command.clear()] })
    
    def test_action_account_move_reversal_wizard(self):
        """ Test reversal wizard creation and validation for Bill of Entry journal entry. """
        self.custom_duty_wizard.action_create_and_post_journal_entry()
        self.assertTrue(self.vendor_bill.bill_of_entry_id, "Bill of Entry journal entry should exist.")

        action = self.custom_duty_wizard.action_account_move_reversal_wizard()
        reversal_wizard = self.env["account.move.reversal"].search([("move_ids", "in", [self.vendor_bill.bill_of_entry_id.id])], limit=1)
        
        self.assertTrue(reversal_wizard, "Reversal wizard should be created.")
        self.assertEqual(reversal_wizard.journal_id, self.custom_duty_wizard.journal_id, "Journal should match for reversal of entry.")

        self.assertEqual(action["res_model"], "account.move.reversal", "Action should open the reversal wizard.")
        self.assertEqual(action["res_id"], reversal_wizard.id, "Reversal wizard ID should match.")
