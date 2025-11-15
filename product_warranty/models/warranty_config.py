from odoo import models, fields


class ProductWarranty(models.Model):
    _name = "warranty.config"
    _description = "This is for warranty configuration"

    name = fields.Char(required=True)
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        ondelete="restrict",
        domain="[('sale_ok', '=', True)]",
        required=True,
    )
    year = fields.Integer(required=True)
    percentage = fields.Float(required=True)
