from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean()
    sub_product_ids = fields.Many2many(comodel_name='product.product', string="Sub Products", required=True, domain=[('is_kit', '!=', True)])
    