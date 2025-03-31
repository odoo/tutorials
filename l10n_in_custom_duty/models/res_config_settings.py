from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_in_custom_duty_enabled = fields.Boolean(related="company_id.l10n_in_custom_duty_enabled", readonly=False)

    # import fields
    import_custom_duty_journal_id = fields.Many2one(comodel_name="account.journal", related="company_id.import_custom_duty_journal_id", readonly=False)
    import_custom_duty_account_id = fields.Many2one(comodel_name="account.account", related="company_id.import_custom_duty_account_id", readonly=False)
    import_default_tax_account_id = fields.Many2one(comodel_name="account.account", related="company_id.import_default_tax_account_id", readonly=False)

    # export fields
    export_custom_duty_journal_id = fields.Many2one(comodel_name="account.journal", related="company_id.export_custom_duty_journal_id", readonly=False)
    export_custom_duty_account_id = fields.Many2one(comodel_name="account.account", related="company_id.export_custom_duty_account_id", readonly=False)
    export_default_tax_account_id = fields.Many2one(comodel_name="account.account", related="company_id.export_default_tax_account_id", readonly=False)
