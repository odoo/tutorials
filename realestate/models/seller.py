from odoo import fields, models


class Seller(models.Model):
    _name = "seller"

    name = fields.Char(required=True)
    properties_ids = fields.One2many("realestate", "seller_id")
