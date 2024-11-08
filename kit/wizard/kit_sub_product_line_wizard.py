from odoo import fields, models


class KitSubProductLineWizard(models.TransientModel):
    _name = "kit.sub.product.line.wizard"

    sub_product_id = fields.Many2one('kit.sub.product.wizard')

    product_id = fields.Many2one('product.product')
    quantity = fields.Float(default=0)
    price = fields.Float()
    sale_order_line_id = fields.Many2one('sale.order.line')
