from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Define the type of the property"

    name = fields.Char(required=True)
