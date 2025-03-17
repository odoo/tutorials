from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_in_custom_duty = fields.Boolean(
        string="Import-Export Custom duty",
        related="company_id.l10n_in_custom_duty",
        readonly=False
    )
    l10n_in_import_journal_id = fields.Many2one(
        "account.journal",
        string="Import default journal",
        domain=[("type", "=", "general")],
        readonly=False,
        related="company_id.l10n_in_import_journal_id"
    )
    l10n_in_import_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Import Custom Duty Account",
        domain=[("account_type", "=", "expense")],
        readonly=False,
        related="company_id.l10n_in_import_custom_duty_account_id"
    )
    l10n_in_import_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Import default tax Account",
        domain=[("account_type", "in", ("asset_current", "liability_current")), ("reconcile", "=", "True")],
        readonly=False,
        related="company_id.l10n_in_import_default_tax_account_id"
    )
    l10n_in_export_journal_id = fields.Many2one(
        "account.journal",
        string="Export default journal",
        domain=[("type", "=", "general")],
        readonly=False,
        related="company_id.l10n_in_export_journal_id"
    )
    l10n_in_export_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Export Custom Duty Account",
        domain=[("account_type", "=", "expense")],
        readonly=False,
        related="company_id.l10n_in_export_custom_duty_account_id"
    )
    l10n_in_export_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Export default tax Account",
        domain=[("account_type", "in", ("asset_current", "liability_current")), ("reconcile", "=", "True")],
        readonly=False,
        related="company_id.l10n_in_export_default_tax_account_id"
    )
