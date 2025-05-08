from odoo import fields, models


class saleOrderLineModularType(models.Model):
    _name = "sale.order.line.modular.type"
    _description = "Modular Type Value for Sale Order Line"

    order_line_id = fields.Many2one("sale.order.line", string="Order Line")
    modular_type_id = fields.Many2one("modular.type", string="Modular Type")
    value = fields.Float(string="Value", required=True)
