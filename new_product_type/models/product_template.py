from odoo import models, fields

class ProductKit(models.Model):
    _inherit = "product.template"
    is_kit = fields.Boolean(string="Is Kit")
    kit_product_ids = fields.Many2many("product.product", "kit_product_m2m", "kit_id", "product_id")