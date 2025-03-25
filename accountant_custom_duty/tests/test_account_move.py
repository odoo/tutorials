from odoo import fields
from odoo.tests import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestAccountMove(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner_overseas = self.env['res.partner'].create({
            'name': 'Overseas Supplier',
            'l10n_in_gst_treatment': 'overseas',
        })
        
        self.journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
        self.expense_account = self.env['account.account'].search([('account_type', '=', 'expense')], limit=1)
        
        self.bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_overseas.id,
            'invoice_date': fields.Date.today(),
            'journal_id': self.journal.id,
            'state': 'draft',
            'line_ids': [(0, 0, {
                'name': 'Test Product',
                'quantity': 1,
                'price_unit': 1000.0,
                'account_id': self.expense_account.id,
            })]
        })
        self.bill.action_post()

    def test_action_open_wizard(self):
        """Test that the Bill of Entry Wizard opens with correct context."""
        action = self.bill.action_open_wizard()
        self.assertEqual(action["res_model"], "account.bill.of.entry.wizard")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_move_id"], self.bill.id)
        self.assertEqual(action["context"]["default_l10n_in_reference"], self.bill.name)
    
    def test_wizard_computations(self):
        """Test computed fields in Account Move Line Wizard."""
        self.wizard = self.env['account.bill.of.entry.wizard'].create({
            'move_id': self.bill.id,
            'l10n_in_custom_currency_rate': 1.2,
        })
        
        self.line = self.env['account.move.line.wizard'].create({
            'wizard_id': self.wizard.id,
            'quantity': 10,
            'price_unit': 200,
            'l10n_in_custom_duty_additional': 50,
            'tax_ids': [(6, 0, self.env['account.tax'].search([('type_tax_use', '=', 'purchase')], limit=1).ids)],
        })

        self.line._compute_l10n_in_assessable_value()
        self.line._compute_l10n_in_taxable_amount()
        self.line._compute_l10n_in_tax_amount()
        
        expected_assessable_value = 10 * 200 * 1.2
        expected_taxable_amount = expected_assessable_value + 50
        expected_tax_amount = sum((expected_taxable_amount * tax.amount) / 100 for tax in self.line.tax_ids)

        self.assertEqual(self.line.l10n_in_assessable_value, expected_assessable_value, "Assessable Value computation is incorrect.")
        self.assertEqual(self.line.l10n_in_taxable_amount, expected_taxable_amount, "Taxable Amount computation is incorrect.")
        self.assertEqual(self.line.l10n_in_tax_amount, expected_tax_amount, "Total Tax Amount computation is incorrect.")

    def test_journal_entry_creation(self):
        """Test that confirming the wizard creates a journal entry."""
        self.wizard = self.env['account.bill.of.entry.wizard'].create({
            'move_id': self.bill.id,
            'l10n_in_custom_currency_rate': 1.2,
        })
        
        self.wizard.action_confirm()
        journal_entry = self.env['account.move'].search([
            ('name', '=', self.bill.name),
            ('journal_id', '=', self.journal.id),
            ('state', '=', 'posted')
        ], limit=1)
        
        self.assertTrue(journal_entry, "Journal entry was not created.")
        self.assertEqual(journal_entry.state, 'posted', "Journal entry is not posted.")
