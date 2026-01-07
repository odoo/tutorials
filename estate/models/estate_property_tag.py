from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tags to describe property such new, renovated...'

    name = fields.Char(required=True)
    
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        "Property Tag must be unique."
    )
