from odoo import fields, models


class SaleOrderLineDistribution(models.Model):
    _name = "sale.order.line.distribution"

    source_order_line_id = fields.Many2one("sale.order.line")
    destination_order_line_id = fields.Many2one("sale.order.line")
    price = fields.Float()
