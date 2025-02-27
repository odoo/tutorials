from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean()
    selected_product_ids = fields.Many2many('product.product', store=True)
