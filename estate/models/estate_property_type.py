from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Define a type of property"

    name = fields.Char(required=True)