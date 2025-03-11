from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    module_account_import_export_duty = fields.Boolean(
        string=_('Import - Export'),
        default=False
    )
