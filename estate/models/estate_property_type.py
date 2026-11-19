from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'This property type name already exists'
    )

    name = fields.Char(required=True, string='Title')
