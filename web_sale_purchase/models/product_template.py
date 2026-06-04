from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    seller_id = fields.Many2one(
        "res.partner",
        domain=[("is_seller", "=", "True")],
        string="Seller Info",
        help="The marketplace vendor who owns and sells this product listing.",
        option="{'no_create': True}",
    )
