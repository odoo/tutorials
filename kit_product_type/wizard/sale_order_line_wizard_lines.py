from odoo import fields, models


class SaleOrderLines(models.TransientModel):
    _name = "sale.order.line.wizard.line"
    _description = "sale.order.lines.for.sub.products"

    wizard_id = fields.Many2one("sale.order.line.wizard")
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    wizard_price = fields.Float()
    price = fields.Float()
