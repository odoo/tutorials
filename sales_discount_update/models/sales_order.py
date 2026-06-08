from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount_percentage = fields.Float(
        string="Global Discount Percentage",
        default=0.0,
        copy=False,
    )
