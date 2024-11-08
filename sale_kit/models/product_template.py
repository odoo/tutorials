from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(default=False)
    sub_products_ids = fields.Many2many(comodel_name='product.product')
