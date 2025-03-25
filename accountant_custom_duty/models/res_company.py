from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_in_custom_duty = fields.Boolean(string="Enable Custom Duty", default=False)

    l10n_in_custom_duty_import_journal_id = fields.Many2one(comodel_name="account.journal",string="Import Journal",check_company=True)
    l10n_in_account_custom_duty_income_id = fields.Many2one(comodel_name="account.account",string="Import Custom Duty Income Account",check_company=True)
    l10n_in_import_default_tax_account = fields.Many2one(comodel_name="account.account",string="Import Journal Suspense Account",check_company=True)

    l10n_in_custom_duty_export_journal_id = fields.Many2one(comodel_name="account.journal",string="Export Journal",check_company=True)
    l10n_in_account_custom_duty_expense_income_id = fields.Many2one(comodel_name="account.account",string="Export Custom Duty Expense/Income Account",check_company=True)
    l10n_in_export_default_tax_account = fields.Many2one(comodel_name="account.account",string="Export Journal Suspense Account",check_company=True)

    l10n_in_custom_duty_tax_payable_account = fields.Many2one(comodel_name="account.account",string="Custom Duty Tax Payable Account",check_company=True)
