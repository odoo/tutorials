from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    is_import_export = fields.Boolean(
        string="Enable Import-Export Settings",
        store=True,
    )
    account_imp_journal_id = fields.Many2one(
        "account.journal",
        string="Default Import Journal",
    )
    account_imp_duty_acct_id = fields.Many2one(
        "account.account",
        string="Default Import Custom Duty Account",
    )
    account_imp_tax_acct_id = fields.Many2one(
        "account.account",
        string="Default Import Tax Account",
    )
    account_exp_journal_id = fields.Many2one(
        "account.journal",
        string="Default Export Journal",
    )
    account_exp_duty_acct_id = fields.Many2one(
        "account.account",
        string="Default Export Custom Duty Account",
    )
    account_exp_tax_acct_id = fields.Many2one(
        "account.account",
        string="Default Export Tax Account",
    )
