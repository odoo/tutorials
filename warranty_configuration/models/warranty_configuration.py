from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "warranty order line for selected products !"

    name = fields.Char(
        required=True,
        string="Name",
    )
    product_id = fields.Many2one("product.product", string="Product")
    year = fields.Integer(default=0, required=True)
    percentage = fields.Float(default=0.0, digits=(5, 2), required=True)
