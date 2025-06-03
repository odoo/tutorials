from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string="Is Kit", help="To make product itself kit")
    sub_products_ids = fields.Many2many(comodel_name='product.product', string="Sub Products")
