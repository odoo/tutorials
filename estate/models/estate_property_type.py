from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type Information'

    name = fields.Char(string='Property Type', required=True)

    _check_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.'
    )
