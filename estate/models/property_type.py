from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'estate property type'

    name = fields.Char(string='Type', required=True)
    property_ids = fields.One2many('estate_property', 'property_type_id')

    _name_uniq = models.Constraint(
        'unique (name)',
        "A property type name must be unique",
    )
