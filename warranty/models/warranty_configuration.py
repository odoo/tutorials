from odoo import models, fields


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Warranty Configuration"

    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', 'Product')
    percentage = fields.Float('Percentage')
    years = fields.Integer(string='Number of Years')
