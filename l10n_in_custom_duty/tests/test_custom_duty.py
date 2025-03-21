from odoo.tests import tagged, TransactionCase
from odoo.exceptions import ValidationError, UserError


@tagged('post_install', '-at_install')
class TestL10nInCustomDuty(TransactionCase):
    def setUp(self):
        """Setup test data for Custom Duty Wizard"""
        super().setUp()

        self.company = self.env["res.company"].search([("id", "=", 2)], limit=1)

        self.l10n_in_import_custom_duty_account_id = self.env["account.account"].create({
            "name": "Custom Duty Expense",
            "code": "EXP001",
            "account_type": "expense",
            "company_ids": [self.company.id],
        })

        self.l10n_in_import_default_tax_account_id = self.env["account.account"].create({
            "name": "Import Tax Account",
            "code": "AST001",
            "account_type": "asset_current",
            "reconcile": True,
            "company_ids": [self.company.id],
        })

        self.l10n_in_import_journal_id = self.env["account.journal"].create({
            "name": "Import Journal",
            "type": "general",
            "code": "IMJ",
            "company_id": self.company.id,
        })

        self.company.write({
            "l10n_in_import_journal_id": self.l10n_in_import_journal_id.id,
            "l10n_in_import_custom_duty_account_id": self.l10n_in_import_custom_duty_account_id.id,
            "l10n_in_import_default_tax_account_id": self.l10n_in_import_default_tax_account_id.id,
        })

        self.currency = self.env["res.currency"].search([("name", "=", "INR")], limit=1)

        self.partner = self.env["res.partner"].create({
            "name": "Test Vendor",
            "company_id": self.company.id,
        })

        self.product = self.env["product.product"].create({
            "name": "Imported Product",
            "categ_id": self.env.ref("product.product_category_all").id,
            "company_id": self.company.id,
        })

        self.journal_id = self.env["account.journal"].create({
            "name": "Vendor Bills",
            "type": "purchase",
            "code": "BILLO",
            "company_id": self.company.id,
        })

        self.bill = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "currency_id": self.currency.id,
            "state": "draft",
            "journal_id": self.journal_id.id,
            "l10n_in_gst_treatment": "overseas",
            "company_id": self.company.id,
        })

        self.bill_line = self.env["account.move.line"].create({
            "move_id": self.bill.id,
            "product_id": self.product.id,
            "quantity": 10,
            "price_unit": 500,
            "account_id": self.l10n_in_import_custom_duty_account_id.id,
            "company_id": self.company.id,
        })

        self.bill.write({
            "state" : "posted"
        })

        self.wizard = self.env["l10n_in.custom.duty.wizard"].create({
            "move_id": self.bill.id,
            "company_id": self.company.id,
            "custom_currency_rate": 1.2
        })

    def test_action_open_wizard(self):
        """Test that the Custom Duty Wizard opens with correct context."""
        action = self.bill.action_l10n_in_custom_duty_wizard()
        self.assertEqual(action["res_model"], "l10n_in.custom.duty.wizard")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["move_id"], self.bill.id)

    def test_wizard_computations(self):
        """Test computed fields in Custom Duty Wizard."""
        self.line = self.env["l10n_in.custom.duty.line"].create({
            "wizard_id": self.wizard.id,
            "bill_id": self.bill.id,
            "move_line_id": self.bill_line.id,
            "quantity": 10,
            "unit_price": 500,
            "custom_duty": 50,
            "tax_ids": [(6, 0, self.env["account.tax"].search([("type_tax_use", "=", "purchase")], limit=1).ids)],
        })

        self.line._compute_assessable_value()
        self.line._compute_taxable_amount()
        self.line._compute_tax_amount()

        expected_assessable_value = 10 * 500 * 1.2
        expected_taxable_amount = expected_assessable_value + 50
        expected_tax_amount = sum((expected_taxable_amount * tax.amount) / 100 for tax in self.line.tax_ids)

        self.assertEqual(self.line.assessable_value, expected_assessable_value, "Assessable Value computation is incorrect.")
        self.assertEqual(self.line.taxable_amount, expected_taxable_amount, "Taxable Amount computation is incorrect.")
        self.assertEqual(self.line.tax_amount, expected_tax_amount, "Total Tax Amount computation is incorrect.")

    def test_journal_entry_creation(self):
        """Test that confirming the wizard creates a journal entry."""
        self.wizard.journal_id = self.journal_id
        self.wizard.line_ids.create({
            "wizard_id": self.wizard.id,
            "bill_id": self.bill.id,
            "move_line_id": self.bill_line.id,
            "custom_duty": 200,
            "taxable_amount": 200,
        })

        self.wizard.action_create_and_post_journal_entry()
        journal_entry = self.env["account.move"].search([
            ("name", "=", self.bill.name),
            ("journal_id", "=", self.journal_id.id),
            ("state", "=", "posted"),
        ], limit=1)

        self.assertTrue(journal_entry, "Journal entry was not created.")
        self.assertEqual(journal_entry.state, "posted", "Journal entry is not posted.")

    def test_prevent_duplicate_journal_entry(self):
        """Test that duplicate journal entries cannot be created"""
        self.wizard.journal_id = self.journal_id
        self.wizard.line_ids.create({
            "wizard_id": self.wizard.id,
            "bill_id": self.bill.id,
            "move_line_id": self.bill_line.id,
            "custom_duty": 200,
            "taxable_amount": 200,
        })
        self.wizard.action_create_and_post_journal_entry()
        journal_entry = self.env["account.move"].search([("ref", "=", self.bill.name)])
        self.assertTrue(journal_entry, "Journal Entry should be created.")
        with self.assertRaises(UserError, msg="A duplicate journal entry should not be allowed."):
            self.wizard.action_create_and_post_journal_entry()

    def test_custom_duty_line_negative_values(self):
        """Test that custom duty and tax amount cannot be negative"""
        with self.assertRaises(ValidationError):
            self.env["l10n_in.custom.duty.line"].create({
                "wizard_id": self.wizard.id,
                "bill_id": self.bill.id,
                "move_line_id": self.bill_line.id,
                "custom_duty": -10,
            })

        with self.assertRaises(ValidationError):
            self.env["l10n_in.custom.duty.line"].create({
                "wizard_id": self.wizard.id,
                "bill_id": self.bill.id,
                "move_line_id": self.bill_line.id,
                "tax_amount": -5,
            })
