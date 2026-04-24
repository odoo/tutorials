from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'
    _rec_name = 'name'

    _unique_property_type = models.Constraint(
        'UNIQUE (name)',
        'The Property Type must be Unique',
    )

    name = fields.Char(required=True)
