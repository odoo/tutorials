from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Warranty configuration for all products"

    name = fields.Char(required=True)
    period = fields.Integer(
        string="Warranty Period (years)",
        default=1,
        help="Duration of the warranty period in year.",
    )
    percentage = fields.Float(
        required=True,
        help="Percentage of the product price to be charged for the warranty.",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        help="Product used to represent the warranty service.",
    )
