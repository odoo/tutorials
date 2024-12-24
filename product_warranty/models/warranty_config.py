from odoo import fields, models

class WarrantyConfig(models.Model):
    _name = "warranty.config"
    _description = "Warranty Config"

    name = fields.Char(required=True, string="Name")
    product_id = fields.Many2one("product.template",  string="Product")
    percentage = fields.Float(string="Percentage", required=True)
    duration = fields.Integer(string="Duration (Years)", required=True, default=0)
