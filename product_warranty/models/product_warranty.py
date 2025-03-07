from odoo import models, fields


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Product Warranty"

    name = fields.Char("Name", required=True)
    percentage = fields.Float("Percentage", required=True)
    product_template_id = fields.Many2one(
        "product.template", string="Product", required=True
    )
    year = fields.Integer("Year", required=True)
