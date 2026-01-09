from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    isKit = fields.Boolean(default=False)
    sub_products = fields.Many2many('product.product')
