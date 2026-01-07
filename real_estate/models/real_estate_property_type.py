from odoo import fields, models


class RealEstateTag(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'real.estate',
        'property_type_id',
        string='Properties'
    )
    _unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )
