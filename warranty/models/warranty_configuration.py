from odoo import models, fields


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"

    name = fields.Char()
    product_id = fields.Many2one("product.product", string="product")
    period = fields.Integer("Period")
    percentage = fields.Float()
