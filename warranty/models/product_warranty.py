from odoo import models, fields


class ProductWarranty(models.Model):
    _name = 'product.warranty'
    _description = 'Product Warranty'

    name = fields.Char(string="Warranty Name", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    percentage = fields.Float(string="Percentage")
    year = fields.Integer(string="Year")
