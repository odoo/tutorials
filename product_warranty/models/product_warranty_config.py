# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductWarrantyConfig(models.Model):
    _name = "product.warranty.config"
    _description = "Product Warranty Configuration"

    name = fields.Char(string="Warranty Name", required=True)
    percentage = fields.Float(string="Percentage", help="Warranty percentage")
    year = fields.Integer(
        string="Warranty Period (Year)", required=True,
        help="Warranty period in years"
    )
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product",
        help="Warranty product name"
    )
