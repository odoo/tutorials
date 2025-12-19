from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char("Property Type", required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique'
    )
