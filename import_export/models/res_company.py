from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    import_export_duty = fields.Boolean()
    import_journal_id = fields.Many2one(
        comodel_name="account.journal", string="Import journal"
    )
    import_custom_duty_account_id = fields.Many2one(
        comodel_name="account.account", string="Import custom duty account"
    )
    import_default_tax_account_id = fields.Many2one(
        comodel_name="account.account", string="Import default tax account"
    )
    export_journal_id = fields.Many2one(
        comodel_name="account.journal", string="Export journal"
    )
    export_custom_duty_account_id = fields.Many2one(
        comodel_name="account.account", string="Export custom duty account"
    )
    export_default_tax_account_id = fields.Many2one(
        comodel_name="account.account", string="Export default tax account"
    )

    def write(self, vals):
        if "import_default_tax_account_id" in vals:
            self.import_default_tax_account_id.reconcile = True

        if "export_default_tax_account_id" in vals:
            self.export_default_tax_account_id.reconcile = True

        if vals.get("import_export_duty") is False:
            vals.update(
                {
                    "import_journal_id": False,
                    "import_custom_duty_account_id": False,
                    "import_default_tax_account_id": False,
                    "export_journal_id": False,
                    "export_custom_duty_account_id": False,
                    "export_default_tax_account_id": False,
                }
            )
        return super().write(vals)
