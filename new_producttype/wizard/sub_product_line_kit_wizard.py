from odoo import fields, models


class SubProductLineKitWizard(models.TransientModel):
    _name = 'sub.product.line.kit.wizard'

    sub_products_line_id = fields.Many2one('sub.product.kit.wizard')
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(default=0.0)
    price = fields.Float(default=0)
