from odoo import fields, models


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Product Warranty"

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    percentage = fields.Float(string="Warranty Percentage", required=True)
    year = fields.Integer(string="Warranty Year", required=True)

    _sql_constraints = [
        (
            "unique_name",
            "UNIQUE(name)",
            "Product Warranty name should be unique.",
        )
    ]
