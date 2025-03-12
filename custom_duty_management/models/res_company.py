from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_in_enable_custom_duty = fields.Boolean()

    # Import

    l10n_in_import_journal_id = fields.Many2one(
        "account.journal",
        string="Import Journal",
        domain=[("type", "=", "general")],
    )
    l10n_in_import_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Custom Duty Account (Import)",
        domain=[("account_type", "=", "expense")],
    )
    l10n_in_import_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Default Tax Account (Import)",
        domain=[
            (
                "account_type",
                "in",
                ["asset_current", "liabilities_current"],
                ("reconcile", "=", True),
            )
        ],
    )

    # Export

    l10n_in_export_journal_id = fields.Many2one(
        "account.journal",
        string="Export Journal",
        domain=[("type", "=", "general")],
    )

    l10n_in_export_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Custom Duty Account (Export)",
        domain=[("account_type", "in", ["expense", "income"])],
    )
    l10n_in_export_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Default Tax Account (Export)",
        domain=[
            ("account_type", "in", ["asset_current", "liabilities_current"]),
            ("reconcile", "=", True),
        ],
    )
