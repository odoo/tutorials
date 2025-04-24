from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Adds different property types"
    name = fields.Char(required=True)
