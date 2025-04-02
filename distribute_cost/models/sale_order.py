from odoo import models, fields


class OrderSale(models.Model):
    _inherit = 'sale.order'

    isDivisionVisible = fields.Boolean(string='division coloumn visible', default=False, store=True)
