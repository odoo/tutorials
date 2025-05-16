from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    # default import config fields
    account_import_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Default Import Journal",
        related='company_id.account_import_journal_id',
        readonly=False
    )
    account_import_custom_duty_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Default Import Custom Duty Account",
        related='company_id.account_import_custom_duty_account_id',
        readonly=False
    )
    account_import_tax_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Default Import Tax Account",
        related='company_id.account_import_tax_account_id',
        readonly=False
    )
    
    # default export config fields
    account_export_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Default Export Journal",
        related='company_id.account_export_journal_id',
        readonly=False
    )
    account_export_custom_duty_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Default Export Custom Duty Account",
        related='company_id.account_export_custom_duty_account_id',
        readonly=False
    )
    account_export_tax_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Default Export Tax Account",
        related='company_id.account_export_tax_account_id',
        readonly=False
    )
