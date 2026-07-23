from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Table for type of property"

    name = fields.Char(required=True)
