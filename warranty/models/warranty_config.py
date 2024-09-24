from odoo import models, fields


class WarrantyConfig(models.Model):
    _name = "warranty.config"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    period = fields.Integer(string="Warranty Years", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    percentage = fields.Float(string="Percentage", required=True)
