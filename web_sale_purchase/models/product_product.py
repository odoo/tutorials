from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    seller_id = fields.Many2one("res.partner")
