from odoo import fields, models


class SaleOrderLines(models.TransientModel):
    _name = "sale.order.line.wizard"
    _description = "sale.order.lines.for.sub.products"

    wizard_id = fields.Many2one("sale.order.wizard")
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    wizard_price = fields.Float()
    price = fields.Float()
