from odoo import api, models, fields
from odoo.exceptions import ValidationError

class ProductWarranty(models.Model):
    _name = 'product.warranty'
    _description = 'Product Warranty'

    name = fields.Char(string="Warranty Name", required=True)
    product_id = fields.Many2one('product.template', string="Product", required=True)
    percentage = fields.Float(string="Warranty Percentage", required=True)
    year = fields.Integer(string="Warranty Year")
