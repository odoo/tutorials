from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    custom_duty = fields.Boolean(string="Enable Custom Duty", default=False)

    import_journal_id = fields.Many2one(comodel_name="account.journal", string="Import Journal", check_company=True)
    import_duty_account_id = fields.Many2one(comodel_name="account.account", string="Import Custom Duty Income Account", check_company=True)
    import_duty_tax_account_id = fields.Many2one(comodel_name="account.account", string="Import Journal Suspense Account", check_company=True)

    export_journal_id = fields.Many2one(comodel_name="account.journal", string="Export Journal", check_company=True)
    export_duty_account_id = fields.Many2one(comodel_name="account.account", string="Export Custom Duty Expense/Income Account", check_company=True)
    export_duty_tax_account_id = fields.Many2one(comodel_name="account.account", string="Export Journal Suspense Account", check_company=True)
