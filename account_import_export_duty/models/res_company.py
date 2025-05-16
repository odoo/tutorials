from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    account_import_journal_id = fields.Many2one(
        'account.journal', 
        string="Default Import Journal"
    )
    account_import_custom_duty_account_id = fields.Many2one(
        'account.account', 
        string="Default Import Custom Duty Account"
    )
    account_import_tax_account_id = fields.Many2one(
        'account.account', 
        string="Default Import Tax Account"
    )

    account_export_journal_id = fields.Many2one(
        'account.journal', 
        string="Default Export Journal"
    )
    account_export_custom_duty_account_id = fields.Many2one(
        'account.account', 
        string="Default Export Custom Duty Account"
    )
    account_export_tax_account_id = fields.Many2one(
        'account.account', 
        string="Default Export Tax Account"
    )
