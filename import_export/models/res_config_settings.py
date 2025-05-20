from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    import_export_duty = fields.Boolean(
        related="company_id.import_export_duty", readonly=False
    )
    import_journal_id = fields.Many2one(
        comodel_name="account.journal",
        related="company_id.import_journal_id",
        readonly=False,
        help="Journal used for Import Transactions.",
        domain=[("type", "=", "general")],
    )
    import_custom_duty_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.import_custom_duty_account_id",
        readonly=False,
        help="Account used for custom duty import Transactions",
        domain=[("account_type", "=", "expense")],
    )
    import_default_tax_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.import_default_tax_account_id",
        readonly=False,
        help="Account used for default tax import Transactions",
        domain=[("account_type", "in", ["liability_current", "asset_current"])],
    )
    export_journal_id = fields.Many2one(
        comodel_name="account.journal",
        related="company_id.export_journal_id",
        readonly=False,
        help="Journal used for Import Transactions.",
    )
    export_custom_duty_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.export_custom_duty_account_id",
        readonly=False,
        help="Account used for custom duty export Transactions",
        domain=[("account_type", "in", ["expense", "income"])],
    )
    export_default_tax_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.export_default_tax_account_id",
        readonly=False,
        help="Account used for default tax import Transactions",
        domain=[("account_type", "in", ["liability_current", "asset_current"])],
    )
