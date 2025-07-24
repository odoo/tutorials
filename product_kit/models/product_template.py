from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean()
    kit_product_ids = fields.Many2many('product.product', store=True)
