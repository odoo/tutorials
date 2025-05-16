from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


@tagged('post_install', '-at_install')
class TestBillEntryWizard(TransactionCase):

    def setUp(self):
        super().setUp()
        
        self.company_id = self.env.ref('base.main_company').id
        self.wizard_model = self.env['bill.entry.wizard']
        self.bill_entry_model = self.env['bill.entry.details']
        self.journal_model = self.env['account.journal']
        self.account_move_model = self.env['account.move']
        self.account_move_line_model = self.env['account.move.line']
        
        self.custom_duty_account = self.env['account.account'].create({
            'name': 'Custom Duty Account',
            'code': 'CUSTOM',
            'account_type': 'expense',
        })
        
        self.tax_account = self.env['account.account'].create({
            'name': 'Tax Account',
            'code': 'TAX',
            'account_type': 'liability_current',
        })
        
        self.import_journal = self.journal_model.create({
            'name': 'Import Journal',
            'code': 'IMPORT',
            'type': 'general',
            'default_account_id': self.custom_duty_account.id,
        })
        
        self.env.company.write({
            'account_import_journal_id': self.import_journal.id,
            'account_import_custom_duty_account_id': self.custom_duty_account.id,
            'account_import_tax_account_id': self.tax_account.id,
        })
        
        self.vendor_bill = self.account_move_model.create({
            'move_type': 'in_invoice',
            'partner_id': self.company_id,
            'state': 'draft',
            'l10n_in_gst_treatment': 'overseas',
        })
    
        self.wizard = self.wizard_model.create({
            'move_id': self.vendor_bill.id,
        })
        
        self.product = self.env.ref('product.product_product_4')
        self.line_id = self.account_move_line_model.create({
            'move_id': self.vendor_bill.id,
            'product_id': self.product.id,
            'quantity': 1,
            'price_unit': 100,
            'account_id': self.custom_duty_account.id,
        })
        
        self.bill_entry = self.bill_entry_model.create({
            'move_line_id': self.line_id.id,
            'wizard_id': self.wizard.id,
            'custom_duty': 100,
            'tax_amount': 50
        })
        
        self.vendor_bill.state = 'posted'
    
    def test_open_bill_of_entry_wizard_with_invalid_state(self):
        self.vendor_bill.state = 'draft'
        
        with self.assertRaises(UserError):
            self.vendor_bill.action_open_bill_of_entry_wizard()
    
    def test_open_bill_of_entry_wizard_with_valid_state(self):
        self.vendor_bill.state = 'posted'
        self.vendor_bill.l10n_in_gst_treatment = 'overseas'
        
        action = self.vendor_bill.action_open_bill_of_entry_wizard()
        self.assertEqual(action['res_model'], 'bill.entry.wizard')
        self.assertEqual(action['view_mode'], 'form')
        self.assertEqual(action['target'], 'new')
        self.assertEqual(action['context']['move_id'], self.vendor_bill.id)

    def test_currency_rate_zero_validation(self):
        with self.assertRaises(ValidationError):
            self.wizard.custom_currency_rate = 0

    def test_currency_rate_negative_validation(self):
        with self.assertRaises(ValidationError):
            self.wizard.custom_currency_rate = -1
            
    def test_negative_custom_duty(self):
        temp = self.bill_entry_model.create({
            'move_line_id': self.line_id.id,
            'wizard_id': self.wizard.id
        })
        
        with self.assertRaises(ValidationError):
            temp.write({
                'custom_duty': -100,
            })

    def test_journal_entry_creation_with_no_lines(self):
        empty_wizard = self.wizard_model.create({
            'move_id': self.vendor_bill.id,
        })
        
        with self.assertRaises(UserError):
            empty_wizard.action_create_and_post_journal_entry()

    def test_journal_entry_creation_with_no_values(self):
        self.bill_entry_model.create({
            'move_line_id': self.line_id.id,
            'wizard_id': self.wizard.id,
        })
        
        with self.assertRaises(UserError):
            self.wizard.action_create_and_post_journal_entry()
            
    def test_missing_custom_duty_and_tax_validation(self):
        draft_bill = self.account_move_model.create({
            'move_type': 'in_invoice',
            'partner_id': self.company_id,
            'state': 'draft',
            'l10n_in_gst_treatment': 'overseas',
        })
        
        wizard = self.wizard_model.create({
            'move_id': draft_bill.id,
        })
        
        with self.assertRaises(UserError):
            wizard.action_create_and_post_journal_entry()

    def test_journal_entry_creation_and_verification(self):
        self.wizard.action_create_and_post_journal_entry()
        
        journal_entry = self.vendor_bill.custom_duty_journal_entry_id
        self.assertTrue(journal_entry)
        self.assertEqual(journal_entry.state, 'posted')
        self.assertEqual(len(journal_entry.line_ids), 3)

    def test_journal_entry_reset_to_draft_functionality(self):
        self.wizard.action_create_and_post_journal_entry()
        
        journal_entry = self.vendor_bill.custom_duty_journal_entry_id
        self.assertTrue(journal_entry)
        
        self.wizard.custom_duty_journal_entry_id = journal_entry.id
        self.wizard.button_draft_journal_entry()
        self.assertEqual(journal_entry.state, 'draft')
