from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Import
    l10n_in_import_journal_id = fields.Many2one("account.journal", domain=[("type", "=", "general")],)
    l10n_in_import_custom_duty_account_id = fields.Many2one("account.account", domain=[("account_type", "=", "expense")],)
    l10n_in_import_custom_duty_tax_payable_account_id = fields.Many2one("account.account", domain=[("account_type", "=", "liability_current")],)
    l10n_in_import_default_tax_account_id = fields.Many2one(
        "account.account",
        domain=[
            ("account_type", "in", ["asset_current", "liability_current"]),
            ("reconcile", "=", True),
        ],
    )

    # Export
    l10n_in_export_journal_id = fields.Many2one("account.journal", domain=[("type", "=", "general")],)
    l10n_in_export_custom_duty_account_id = fields.Many2one("account.account", domain=[("account_type", "in", ["expense", "income"])],)
    l10n_in_export_custom_duty_tax_payable_account_id = fields.Many2one("account.account", domain=[("account_type", "=", "liability_current")],)
    l10n_in_export_default_tax_account_id = fields.Many2one(
        "account.account",
        domain=[
            ("account_type", "in", ["asset_current", "liability_current"]),
            ("reconcile", "=", True),
        ],
    )
