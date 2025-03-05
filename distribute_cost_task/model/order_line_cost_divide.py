from odoo import fields, models


class OrderLineCostDivide(models.Model):
    _name = 'order.line.cost.divide'
    _description='order line cost divide'

    cost = fields.Float("Divided Cost")
    divide_from_order_line = fields.Many2one("sale.order.line", string = "Divide from order line")
    divide_to_order_line = fields.Many2one("sale.order.line", string="Divide to Order Line")
    order_id = fields.Many2one("sale.order", string="Order Id", required=True)
