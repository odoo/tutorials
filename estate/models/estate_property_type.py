from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Test property type description"

    name = fields.Char(required=True)
