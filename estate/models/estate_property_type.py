from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Contains the different types of properties"

    name = fields.Char(required=True)
