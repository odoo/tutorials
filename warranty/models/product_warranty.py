from odoo import models, fields


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Warranty"

    name = fields.Char(string="Name", required=True)
    duration = fields.Integer(string="Duration(in years)")
    product_id = fields.Many2one("product.product", string="Product")
    percentage = fields.Float(string="Percentage", required=True)
