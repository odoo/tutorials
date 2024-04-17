from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describes the type of a property"

    name = fields.Char(required=True)
    