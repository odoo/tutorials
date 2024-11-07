from odoo import fields, models


class WarrantyProduct(models.TransientModel):
    _name = 'product.wizard'
    _description = 'product wizard description'

    product_id = fields.Many2one(
        'product.product'
    )
    quantity = fields.Integer(default=0)
    price = fields.Integer(default=0)

    wizard_kit_id = fields.Many2one(
        'kit.wizard'
    )
    sale_order_line_id = fields.Many2one('sale.order.line')
