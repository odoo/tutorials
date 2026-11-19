from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char('Type', required=True)

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a property type must be unique.',
    )
