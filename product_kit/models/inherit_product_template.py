from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean('Is a Kit', default=False, help="Check if this product is a kit")
    sub_products = fields.Many2many('product.product', string='Sub Products')
