from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    
    _inherit = 'res.config.settings'
    
    pos_simplified_receipt = fields.Boolean(related='pos_config_id.simplified_receipt', readonly=False)
