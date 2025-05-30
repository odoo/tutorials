from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_import_export = fields.Boolean(
        string="Enable Import-Export Settings",
        company_dependent=True,
        store=True,
    )
    account_imp_journal_id = fields.Many2one(
        "account.journal",
        string="Default Import Journal",
        related="company_id.account_imp_journal_id",
        readonly=False,
    )
    account_imp_duty_acct_id = fields.Many2one(
        "account.account",
        string="Default Import Custom Duty Account",
        related="company_id.account_imp_duty_acct_id",
        readonly=False,
    )
    account_imp_tax_acct_id = fields.Many2one(
        "account.account",
        string="Default Import Tax Account",
        related="company_id.account_imp_tax_acct_id",
        readonly=False,
    )
    account_exp_journal_id = fields.Many2one(
        "account.journal",
        string="Default Export Journal",
        related="company_id.account_exp_journal_id",
        readonly=False,
    )
    account_exp_duty_acct_id = fields.Many2one(
        "account.account",
        string="Default Export Custom Duty Account",
        related="company_id.account_exp_duty_acct_id",
        readonly=False,
    )
    account_exp_tax_acct_id = fields.Many2one(
        "account.account",
        string="Default Export Tax Account",
        related="company_id.account_exp_tax_acct_id",
        readonly=False,
    )
