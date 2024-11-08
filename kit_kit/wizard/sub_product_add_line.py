from odoo import api, fields, models


class SubProductAddLine(models.TransientModel):
    _name = "sub.product.add.line"

    sub_product_id = fields.Many2one("sub.product.wizard")

    product_id = fields.Many2one("product.product")
    quantity = fields.Integer(string="Quantity", default=0)
    price = fields.Float()
    sale_order_line_id = fields.Many2one('sale.order.line')
