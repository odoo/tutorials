from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(
        string='Is a Kit'
        )
    sub_product_ids = fields.Many2many(
        comodel_name='product.product', 
        string="Sub Products", 
        required=True, 
        domain=[('is_kit', '!=', True)]
        )
