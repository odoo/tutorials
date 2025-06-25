from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_deposit = fields.Many2one('product.product', string="Deposit",
                                      related="company_id.product_deposit",
                                      readonly=False, domain=[("rent_ok", "=", True)])
