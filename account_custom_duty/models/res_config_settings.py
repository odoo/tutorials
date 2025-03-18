from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_import_export = fields.Boolean(string="Enable Import-Export Settings", company_dependent=True, store=True)
    
    # default import config fields
    account_import_journal_id = fields.Many2one(
        'account.journal',
        string="Default Import Journal",
        related='company_id.account_import_journal_id',
        readonly=False
    )
    account_import_custom_duty_account_id = fields.Many2one(
        'account.account',
        string="Default Import Custom Duty Account",
        related='company_id.account_import_custom_duty_account_id',
        readonly=False
    )
    account_import_tax_account_id = fields.Many2one(
        'account.account',
        string="Default Import Tax Account",
        related='company_id.account_import_tax_account_id',
        readonly=False
    )
    
    # default export config fields
    account_export_journal_id = fields.Many2one(
        'account.journal',
        string="Default Export Journal",
        related='company_id.account_export_journal_id',
        readonly=False
    )
    account_export_custom_duty_account_id = fields.Many2one(
        'account.account',
        string="Default Export Custom Duty Account",
        related='company_id.account_export_custom_duty_account_id',
        readonly=False
    )
    account_export_tax_account_id = fields.Many2one(
        'account.account',
        string="Default Export Tax Account",
        related='company_id.account_export_tax_account_id',
        readonly=False
    )
