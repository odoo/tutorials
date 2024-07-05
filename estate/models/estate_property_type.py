from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Properties Type defined"

    name = fields.Char(required=True)
