from odoo import fields, models


class Owner(models.Model):
    _name = "owner"

    name = fields.Char(required=True)
    address = fields.Char()
    phone = fields.Char()
    properties_ids = fields.One2many("realestate", "owner_id")
