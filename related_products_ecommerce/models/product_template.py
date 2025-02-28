from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    related_product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='related_product_relation',
        column1='product_id',
        column2='related_id',
        string="Related Products"
    )
