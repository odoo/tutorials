from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_in_custom_duty = fields.Boolean(related="company_id.l10n_in_custom_duty", readonly=False, help="Enable Custom Duty.")
    l10n_in_custom_duty_tax_payable_account = fields.Many2one(comodel_name="account.account", related="company_id.l10n_in_custom_duty_tax_payable_account", readonly=False, help="Import and Export tax payable account.")

    # Import
    l10n_in_custom_duty_import_journal_id = fields.Many2one(comodel_name="account.journal", related="company_id.l10n_in_custom_duty_import_journal_id", readonly=False, help="Journal used for import custom duty.")
    l10n_in_account_custom_duty_income_id = fields.Many2one(comodel_name="account.account", related="company_id.l10n_in_account_custom_duty_income_id", readonly=False, domain="[('account_type', '=', 'expense')]", help="Import custom duty account.")
    l10n_in_import_default_tax_account = fields.Many2one(comodel_name="account.account", related="company_id.l10n_in_import_default_tax_account", readonly=False, domain="[('reconcile', '=', True), ('deprecated', '=', False), ('account_type', 'in', ('asset_current', 'liability_current'))]", help="Import account which is of type Current Asset or Liability.")

    # Export
    l10n_in_custom_duty_export_journal_id = fields.Many2one(comodel_name="account.journal", related="company_id.l10n_in_custom_duty_export_journal_id", readonly=False, help="Journal used for export custom duty.")
    l10n_in_account_custom_duty_expense_income_id = fields.Many2one(comodel_name="account.account", related="company_id.l10n_in_account_custom_duty_expense_income_id", readonly=False, domain="[('account_type', 'in', ('income', 'expense'))]", help="Export custom duty account.")
    l10n_in_export_default_tax_account = fields.Many2one(comodel_name="account.account", related="company_id.l10n_in_export_default_tax_account", readonly=False, domain="[('reconcile', '=', True), ('deprecated', '=', False), ('account_type', 'in', ('asset_current', 'liability_current'))]", help="Export account which is of type Current Asset or Liability.")

    @api.model
    def get_values(self):
        res = super().get_values()
        company = self.env.company
        
        res.update(
            l10n_in_custom_duty=company.l10n_in_custom_duty,
            l10n_in_custom_duty_import_journal_id=company.l10n_in_custom_duty_import_journal_id.id,
            l10n_in_account_custom_duty_income_id=company.l10n_in_account_custom_duty_income_id.id,
            l10n_in_import_default_tax_account=company.l10n_in_import_default_tax_account.id,
            l10n_in_custom_duty_tax_payable_account=company.l10n_in_custom_duty_tax_payable_account.id,
            l10n_in_custom_duty_export_journal_id=company.l10n_in_custom_duty_export_journal_id.id,
            l10n_in_account_custom_duty_expense_income_id=company.l10n_in_account_custom_duty_expense_income_id.id,
            l10n_in_export_default_tax_account=company.l10n_in_export_default_tax_account.id,
        )
        return res

    def set_values(self):
        super().set_values()
        company = self.env.company

        company.write(
            {
                "l10n_in_custom_duty": self.l10n_in_custom_duty,
                "l10n_in_custom_duty_import_journal_id": self.l10n_in_custom_duty_import_journal_id.id,
                "l10n_in_account_custom_duty_income_id": self.l10n_in_account_custom_duty_income_id.id,
                "l10n_in_import_default_tax_account": self.l10n_in_import_default_tax_account.id,
                "l10n_in_custom_duty_tax_payable_account": self.l10n_in_custom_duty_tax_payable_account.id,
                "l10n_in_custom_duty_export_journal_id": self.l10n_in_custom_duty_export_journal_id.id,
                "l10n_in_account_custom_duty_expense_income_id": self.l10n_in_account_custom_duty_expense_income_id.id,
                "l10n_in_export_default_tax_account": self.l10n_in_export_default_tax_account.id,
            }
        )
