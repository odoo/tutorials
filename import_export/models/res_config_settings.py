from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # General Import-Export Settings
    is_import_export = fields.Boolean(
        string="Enable Import-Export Settings",
        company_dependent=True,
        store=True,
        help="Enable/disable import-export functionality for this company",
    )

    # Import Settings
    account_imp_journal_id = fields.Many2one(
        "account.journal",
        string="Default Import Journal",
        related="company_id.account_imp_journal_id",
        readonly=False,
        help="Default journal to use for import operations",
    )
    account_imp_duty_acct_id = fields.Many2one(
        "account.account",
        string="Default Import Custom Duty Account",
        related="company_id.account_imp_duty_acct_id",
        readonly=False,
        help="Account to use for recording import custom duties",
    )
    account_imp_tax_acct_id = fields.Many2one(
        "account.account",
        string="Default Import Tax Account",
        related="company_id.account_imp_tax_acct_id",
        readonly=False,
        help="Account to use for recording import taxes",
    )

    # Export Settings
    account_exp_journal_id = fields.Many2one(
        "account.journal",
        string="Default Export Journal",
        related="company_id.account_exp_journal_id",
        readonly=False,
        help="Default journal to use for export operations",
    )
    account_exp_duty_acct_id = fields.Many2one(
        "account.account",
        string="Default Export Custom Duty Account",
        related="company_id.account_exp_duty_acct_id",
        readonly=False,
        help="Account to use for recording export custom duties",
    )
    account_exp_tax_acct_id = fields.Many2one(
        "account.account",
        string="Default Export Tax Account",
        related="company_id.account_exp_tax_acct_id",
        readonly=False,
        help="Account to use for recording export taxes",
    )
