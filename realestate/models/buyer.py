from odoo import fields, models


class Buyer(models.Model):
    _name = "buyer"

    name = fields.Char(required=True)
    properties_ids = fields.One2many("realestate", "buyer_id")
