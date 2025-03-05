import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProductWarrantyConfiguration(models.Model):
    _name = "product.warranty"
    _description = "Product Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    product_template_id = fields.Many2one(
        "product.template",
        string="Product Name",
        ondelete="cascade",
        required=True)
    years = fields.Float(string="Year", default=1, digits=(None, 1))
    percentage = fields.Float(string="Percentage")

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Two Warranties can not be of same name"),
        ("percentage_check", "CHECK (percentage BETWEEN 0 AND 100)", "Percentage must be between 0 and 100."),
    ]
     