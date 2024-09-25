from odoo import models, fields


class ProductWarranty(models.Model):
    _name = "product.warranty"

    name = fields.Char("Title")
