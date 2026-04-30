from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'type'
    _rec_name = 'type'

    _unique_property_type = models.Constraint(
        'UNIQUE (type)',
        'The Property Type must be Unique',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=1
    )
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )
    type = fields.Char(required=True)
