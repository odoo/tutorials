from odoo import fields, models


class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "property type"

    name = fields.Char(required=True)
