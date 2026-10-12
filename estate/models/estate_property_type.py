from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _rec_name = 'property_type'
    _order = 'property_type'

    property_type = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer("Sequence", default=1)

    _name_uniq = models.Constraint(
        'unique(property_type)',
        'A property type name must be unique',
    )
