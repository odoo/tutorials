from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _rec_name = 'type'
    _order = 'type'

    colour = fields.Selection(
        [
            ('red', 'Red'),
            ('green', 'Green'),
            ('yellow', 'Yellow')
        ]
    )
    property_ids = fields.One2many(comodel_name='estate.properties', inverse_name='property_type_id')
    type = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE (type)',
        "Property Type should be unique",
    )
