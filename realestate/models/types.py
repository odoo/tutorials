from odoo import fields, models


class Types(models.Model):
    _name = "types"

    name = fields.Char(required=True)
    properties_ids = fields.One2many("realestate", "type_id")
