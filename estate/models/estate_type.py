from odoo import fields, models


class EstateType(models.Model):
    _name = "estate.type"
    _description = "An estate type"

    name = fields.Char(required=True)
