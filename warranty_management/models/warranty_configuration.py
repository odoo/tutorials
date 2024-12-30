from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one(
        "product.product", string="Warranty Product", required=True, ondelete="cascade"
    )
    extended_years = fields.Integer(string="Extended Warranty (Years)", required=True)
    percentage = fields.Float(string="Percentage (%)", required=True)
