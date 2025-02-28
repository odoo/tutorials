from odoo import fields, models

class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Product Warranty"

    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.template", string="Product")
    percentage = fields.Float(string="Warranty Percentage")
    year = fields.Integer(string="Warranty Year")