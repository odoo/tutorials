from odoo import fields
from odoo.tests.common import TransactionCase


class TestBillOfEntry(TransactionCase):
    def setUpClass(self):
        super().setUpClass()

        self.supplier_foreign = self.env["res.partner"].create(
            {
                "name": "Foreign Supplier",
                "l10n_in_gst_treatment": "overseas",
            }
        )
        self.test_product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
            }
        )
        self.journal = self.env["account.journal"].search([("type", "=", "purchase")], limit=1)
        self.cost_account = self.env["account.account"].search([("account_type", "=", "expense")], limit=1)
        self.tax_account = self.env["account.account"].search([("account_type", "=", "liability_current")], limit=1)
        self.custom_duty_account = self.env["account.account"].search([("account_type", "=", "asset_current")], limit=1)
        self.vendor_bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.supplier_foreign.id,
                "invoice_date": fields.Date.today(),
                "journal_id": self.journal.id,
                "state": "draft",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Imported Goods",
                            "quantity": 1,
                            "price_unit": 1000.0,
                            "account_id": self.cost_account.id,
                            "debit": 1000.0,
                            "credit": 0.0,
                            "balance": 1000.0,
                        },
                    )
                ],
            }
        )
        self.vendor_bill.action_post()

        self.env["res.config.settings"].create(
            {
                "l10n_in_import_journal_id": self.journal.id,
                "l10n_in_import_custom_duty_account_id": self.custom_duty_account.id,
                "l10n_in_import_default_tax_account_id": self.cost_account.id,
                "l10n_in_import_custom_duty_tax_payable_account_id": self.tax_account.id,
            }
        ).execute()

    def test_action_open_bill_of_entry_wizard(self):
        """Ensure the Bill of Entry Wizard opens with the correct context."""

        action_data = self.vendor_bill.action_open_bill_of_entry_wizard()
        self.assertEqual(action_data["res_model"], "bill.of.entry.wizard")
        self.assertEqual(action_data["view_mode"], "form")
        self.assertEqual(action_data["target"], "new")
        self.assertEqual(action_data["context"]["default_move_id"], self.vendor_bill.id)
        self.assertEqual(action_data["context"]["default_reference"], self.vendor_bill.name)

    def test_bill_of_entry_calculations(self):
        """Test computed values in the Bill of Entry Wizard."""

        self.entry_wizard = self.env["bill.of.entry.wizard"].create({"move_id": self.vendor_bill.id, "custom_currency_rate": 80.00,})
        purchase_tax = self.env["account.tax"].search([("type_tax_use", "=", "purchase")], limit=1)

        # Bill of Entry Wizard Line
        self.entry_line = self.env["bill.of.entry.line.wizard"].create(
            {
                "product_id": self.test_product.id,
                "wizard_id": self.entry_wizard.id,
                "quantity": 5,
                "price_unit_foreign": 300,
                "custom_duty": 50,
                "tax_id": purchase_tax.id,
            }
        )

        self.entry_line._compute_values()

        # Expected Computed Values
        expected_assessable_value = 5 * 300 * 80
        expected_taxable_amount = expected_assessable_value + 50
        expected_tax_amount = (expected_taxable_amount * purchase_tax.amount) / 100

        self.assertEqual(self.entry_line.assessable_value, expected_assessable_value, "Assessable Value calculation is incorrect.")
        self.assertEqual(self.entry_line.taxable_amount, expected_taxable_amount, "Taxable Amount calculation is incorrect.")
        self.assertEqual(self.entry_line.tax_amount, expected_tax_amount, "Total Tax Amount calculation is incorrect.")

    def test_journal_entry_creation(self):
        """Test if a journal entry is created after confirming Bill of Entry."""
        self.entry_wizard = self.env["bill.of.entry.wizard"].create(
            {
                "move_id": self.vendor_bill.id,
                "custom_currency_rate": 80.00,
            }
        )

        self.entry_wizard.action_confirm()

        journal_entry = self.env["account.move"].search(
            [
                ("name", "=", self.vendor_bill.name),
                ("journal_id", "=", self.journal.id),
                ("state", "=", "posted"),
            ],
            limit=1,
        )

        self.assertTrue(journal_entry, "Journal Entry was not created after confirming Bill of Entry.")
        self.assertEqual(journal_entry.state, "posted", "Journal entry is not posted.")
