from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string="Is Kit", default=False, help="Enable this to sell as a kit")
    sub_products_ids = fields.Many2many('product.product', string="Sub Products")
