from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tags to describe property such new, renovated...'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        "Property Tag must be unique."
    )
