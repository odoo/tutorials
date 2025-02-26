from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    distributed_cost = fields.Float(string="Distributed Cost")
