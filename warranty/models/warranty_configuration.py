from odoo import fields, models


class WarrantyConfig(models.Model):
    _name = "warranty.config"
    _description = "Warranty Configuration for declaring warranty"

    name = fields.Char(string="Name", required=True)
    period = fields.Integer(string="Period", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    percentage = fields.Float(string="Percentage", required=True)
