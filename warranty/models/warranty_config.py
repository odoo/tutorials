from odoo import models, fields


class WarrantyConfig(models.Model):
    _name = "warranty.config"

    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", string="Product")
    percentage = fields.Float(default=0.0)
    period = fields.Integer(default=0)
