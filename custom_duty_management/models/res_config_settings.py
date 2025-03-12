from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_in_enable_custom_duty = fields.Boolean(
        related="company_id.l10n_in_enable_custom_duty",
        readonly=False,
    )

    # Import Fields
    l10n_in_import_journal_id = fields.Many2one(
        related="company_id.l10n_in_import_journal_id", readonly=False
    )
    l10n_in_import_custom_duty_account_id = fields.Many2one(
        related="company_id.l10n_in_import_custom_duty_account_id", readonly=False
    )
    l10n_in_import_default_tax_account_id = fields.Many2one(
        related="company_id.l10n_in_import_default_tax_account_id", readonly=False
    )

    # Export Fields
    l10n_in_export_journal_id = fields.Many2one(
        related="company_id.l10n_in_export_journal_id", readonly=False
    )
    l10n_in_export_custom_duty_account_id = fields.Many2one(
        related="company_id.l10n_in_export_custom_duty_account_id", readonly=False
    )
    l10n_in_export_default_tax_account_id = fields.Many2one(
        related="company_id.l10n_in_export_default_tax_account_id", readonly=False
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        company = self.env.company
        res.update(
            l10n_in_enable_custom_duty=company.l10n_in_enable_custom_duty,
            l10n_in_import_journal_id=company.l10n_in_import_journal_id.id,
            l10n_in_import_custom_duty_account_id=company.l10n_in_import_custom_duty_account_id.id,
            l10n_in_import_default_tax_account_id=company.l10n_in_import_default_tax_account_id.id,
            l10n_in_export_journal_id=company.l10n_in_export_journal_id.id,
            l10n_in_export_custom_duty_account_id=company.l10n_in_export_custom_duty_account_id.id,
            l10n_in_export_default_tax_account_id=company.l10n_in_export_default_tax_account_id.id,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        company = self.env.company
        company.write(
            {
                "l10n_in_enable_custom_duty": self.l10n_in_enable_custom_duty,
                "l10n_in_import_journal_id": self.l10n_in_import_journal_id.id,
                "l10n_in_import_custom_duty_account_id": self.l10n_in_import_custom_duty_account_id.id,
                "l10n_in_import_default_tax_account_id": self.l10n_in_import_default_tax_account_id.id,
                "l10n_in_export_journal_id": self.l10n_in_export_journal_id.id,
                "l10n_in_export_custom_duty_account_id": self.l10n_in_export_custom_duty_account_id.id,
                "l10n_in_export_default_tax_account_id": self.l10n_in_export_default_tax_account_id.id,
            }
        )
