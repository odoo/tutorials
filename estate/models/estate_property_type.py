from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'sequence,name'

    name = fields.Char(required=True)
    sequence = fields.Integer('sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _unique_type = models.Constraint(
        'unique(name)',
        'Property type should be unique'

    )
