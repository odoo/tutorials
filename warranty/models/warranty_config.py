from odoo import fields, models


class WarrantyConfig(models.Model):
    _name = "warranty.config"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", string="Product")
    percentage = fields.Integer(string="Percentage")
    duration = fields.Integer(string="Duration")
