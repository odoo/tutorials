from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string='Is Kit', help='Check this box if the product is a kit that contains other products.', default=False)

    kit_product_ids = fields.Many2many('product.product', string='Sub Products', help='Products included in this kit.')
