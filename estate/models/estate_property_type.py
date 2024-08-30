from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "property type model"

    name = fields.Char(required=True)

    _sql_constraints = [('unique_property_type', 'UNIQUE(name)', 'a property type name must be unique'),
    ]