from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit="product.template"
    
    is_warranty_available = fields.Boolean(string="Is Warranty Available", help="Enabling this field allows the product to be offered as a warranty option.")
