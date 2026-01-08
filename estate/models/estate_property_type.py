from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Defines types of property"

    name = fields.Char(string="Name", required=True)

    _type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )
