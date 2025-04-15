from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _description = "add warranty to product"

    name = fields.Char(string="Warranty name", required=True)
    duration = fields.Integer(string="Duration(in years)")
    percentage = fields.Float(string="Percentage")
    product_id = fields.Many2one('product.template', domain=[("type", "=", "service")], string="Product", ondelete="cascade", required=True)

    _sql_constraints = [
        ("unique_warranty_configuration", "UNIQUE(name, product_id)", "Warranty configuration already exists"),
        ("valid_percentage", "CHECK(percentage > 0)", "Percentage must be greater than zero"),
        ("valid_duration", "CHECK(duration > 0)", "Warranty duration must be greater than zero")
    ]
