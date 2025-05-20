from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "a type of property"

    name = fields.Char(required=True)
