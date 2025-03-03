from odoo import api, fields, models


class ProductWarrantyConfig(models.Model):
    _name = 'product.warranty.config'
    _description = "Product warranty configuration"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique'),
    ]
    
    name = fields.Char(string="Warranty Period", required=True)
    percentage = fields.Float(string="Percentage", required=True)
    year = fields.Integer(string="Year", required=True, help="Number of warranty years.")
    product_template_id = fields.Many2one(
        'product.template',
        string="Product",
        required=True
    )
