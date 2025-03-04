from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    percentage = fields.Float(string="Percentage", required=True)
    years = fields.Integer(string="Years", required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The warranty configuration name should be unique.")
    ]
