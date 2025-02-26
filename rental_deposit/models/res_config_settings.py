from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    extra_deposit = fields.Many2one(
        comodel_name='product.product',
        related='company_id.extra_deposit',
        domain=[('type', '=', 'service')],
        readonly=False,
    )
