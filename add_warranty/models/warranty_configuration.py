from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Allows warranty configuration option"
    _rec_name = "product_id"

    _sql_constraints = [
        ("check_unique_warranty", "UNIQUE(name, product_id)", "Warranty configuration already exists"),
        ("valid_percent", "CHECK(percent >= 0)", "The value of percentage must be positive"),
        ("valid_period", "CHECK(period > 0)", "Period of warranty must be greater than zero")
    ]

    name = fields.Char(string="Name")
    period = fields.Integer(string="Period (in years)")
    product_id = fields.Many2one(
        comodel_name="product.template",
        string="Product",
        domain=[("type", "=", "service")],
        required=True,
        ondelete="cascade")
    percent = fields.Float(string="Percentage")
