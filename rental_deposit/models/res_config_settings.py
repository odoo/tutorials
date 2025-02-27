from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product = fields.Many2one(
        related='company_id.deposit_product_id',
        readonly=False,
    )
