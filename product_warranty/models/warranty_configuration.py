from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "product.warranty.configuration"
    _description = "product.warranty.configuration"

    name = fields.Char(string="name", required=True)
    product_id = fields.Many2one('product.template',required=True)
    percentage = fields.Float()
    years = fields.Integer(default=1)

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Warranty name must be unique."),
        ("percentage_check", "CHECK (percentage >= 0 AND percentage <= 100)", "Percentage must be between 0 and 100."),
        ("years_positive", "CHECK (years > 0)", "Warranty years must be greater than zero."),
    ]
