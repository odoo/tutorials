from odoo import fields, models, api


class SubProuctsLine(models.TransientModel):
    _name = 'sub.products.line'
    _description = "Sub Product Line"

    sub_product_id = fields.Many2one('sub.products')
    product_id = fields.Many2one('product.product')
    product_name = fields.Char(related='product_id.name')
    quantity = fields.Integer()
    price = fields.Float(readonly=False, store=True)
