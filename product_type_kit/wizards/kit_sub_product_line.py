from odoo import fields, models


class KitSubProductLine(models.TransientModel):
    _name = 'kit.sub.product.line'
    _description = 'Kit Sub Product Line'

    wizard_id = fields.Many2one('kit.sub.product.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Price', default=0.0)
