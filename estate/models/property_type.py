from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'estate property type'

    name = fields.Char(string='Type', required=True)

    _name_uniq = models.Constraint(
        'unique (name)',
        "A property type name must be unique",
    )
