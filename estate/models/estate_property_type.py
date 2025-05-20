from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describe the type property"

    name = fields.Char(required=True)