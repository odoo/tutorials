from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "A model where property types are defined"
    _order = "sequence, name, id"
    name = fields.Char(required=True, string="Property Type")
    property_ids = fields.One2many(
        'estate.property', inverse_name='property_type_id', string="Properties")
    sequence = fields.Integer(default=10)

    _unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'Property type must be unique'
    )
