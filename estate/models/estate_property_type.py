from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True)

    _name_unique = models.Constraint(
        'unique(name)',
        'The Property type must be unique.',
    )
