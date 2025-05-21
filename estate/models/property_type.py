from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [('check_estate_property_type_unique', 'UNIQUE (name)', 'The name must be unique.')]
