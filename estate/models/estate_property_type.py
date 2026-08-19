
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type Model'

    name = fields.Char(required=True)
    _check_name = models.Constraint(
        'unique(name)',
        'A property type with this name already exists.',
    )
