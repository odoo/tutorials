from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    account_custom_duty = fields.Boolean(
        string="Import-Export Custom duty",
        related="company_id.account_custom_duty",
        readonly=False
    )
    account_import_journal_id = fields.Many2one(
        "account.journal",
        string="Import default journal",
        domain=[("type", "=", "general")],
        readonly=False,
        related="company_id.account_import_journal_id"
    )
    account_import_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Import Custom Duty Account",
        domain=[("account_type", "=", "expense")],
        readonly=False,
        related="company_id.account_import_custom_duty_account_id"
    )
    account_import_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Import default tax Account",
        domain=[("account_type", "in", ("asset_current", "liability_current")), ("reconcile", "=", "True")],
        readonly=False,
        related="company_id.account_import_default_tax_account_id"
    )
    account_export_journal_id = fields.Many2one(
        "account.journal",
        string="Export default journal",
        domain=[("type", "=", "general")],
        readonly=False,
        related="company_id.account_export_journal_id"
    )
    account_export_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Export Custom Duty Account",
        domain=[("account_type", "=", "expense")],
        readonly=False,
        related="company_id.account_export_custom_duty_account_id"
    )
    account_export_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Export default tax Account",
        domain=[("account_type", "in", ("asset_current", "liability_current")), ("reconcile", "=", "True")],
        readonly=False,
        related="company_id.account_export_default_tax_account_id"
    )
