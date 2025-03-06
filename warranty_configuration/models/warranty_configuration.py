from odoo import models, fields


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one("product.product", string="Extended Warranty", required=True)
    percentage = fields.Float(string="Percentage", required=True)
    duration_years = fields.Integer(string="Duration (Years)", required=True)
