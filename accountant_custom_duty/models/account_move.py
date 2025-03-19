from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    is_confirmed = fields.Boolean(string="Confirmed", default=False)
    l10n_in_journal_entry_number = fields.Char(string="Journal Entry Number")
    l10n_in_company_currency_id = fields.Many2one("res.currency", string="Company Currency ID", default=lambda self: self.env.ref("base.INR"))
    l10n_in_custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="l10n_in_company_currency_id")
    l10n_in_reference = fields.Char(string="Bill Number")
    l10n_in_total_custom_duty = fields.Monetary(string="Total Custom Duty", currency_field="l10n_in_company_currency_id")
    l10n_in_total_l10n_in_tax_amount = fields.Monetary(string="Total Tax Amount", currency_field="l10n_in_company_currency_id")
    l10n_in_total_amount_payable = fields.Monetary(string="Total Amount Payable", currency_field="l10n_in_company_currency_id")

    bill_of_entry_line_ids = fields.One2many("account.move.bill.of.entry.line", "move_id", string="Bill of Entry Details")

    def action_open_wizard(self):
        """Opens the Bill of Entry Wizard."""
        return {
            "type": "ir.actions.act_window",
            "name": "Bill of Entry Wizard",
            "res_model": "account.bill.of.entry.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_move_id": self.id,
                "default_l10n_in_reference": self.name,
                "default_l10n_in_custom_duty_import_journal_id": self.env.company.l10n_in_custom_duty_import_journal_id.id,
                "default_l10n_in_account_custom_duty_income_id": self.env.company.l10n_in_account_custom_duty_income_id.id,
                "default_l10n_in_import_default_tax_account": self.env.company.l10n_in_import_default_tax_account.id,
                "default_l10n_in_custom_duty_tax_payable_account_import": self.env.company.l10n_in_custom_duty_tax_payable_account_import.id,
                "default_l10n_in_shipping_bill_number": self.l10n_in_shipping_bill_number,
                "default_l10n_in_shipping_bill_date": self.l10n_in_shipping_bill_date,
                "default_l10n_in_shipping_port_code_id": self.l10n_in_shipping_port_code_id,
            },
        }

    def action_move_journal_line_bill_of_entry(self):
        """Opens the related journal entry."""
        matching_move = self.env["account.move"].search([("name", "=", self.l10n_in_journal_entry_number)], limit=1)
        if matching_move:
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "views": [[False, "form"]],
                "res_id": matching_move.id,
            }  

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    l10n_in_assessable_value = fields.Monetary(string="Assessable Value")
    l10n_in_custom_duty_additional = fields.Monetary(string="Custom Duty + Additional Charges")
    l10n_in_taxable_amount = fields.Monetary(string="Taxable Amount")
    l10n_in_tax_amount = fields.Monetary(string="Tax Amount")
