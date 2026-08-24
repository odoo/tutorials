from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    size = fields.Selection(
        [('s', 'S'), ('m', 'M'), ('xl', 'XL')],
        string="T-shirt size",
    )
