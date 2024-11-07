from odoo import fields, models


class ProdcutTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean()
    sub_products = fields.Many2many('product.product')
    