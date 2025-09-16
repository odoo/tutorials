from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _order = 'name'

    name = fields.Char("Property Tag", required=True)
    _unique_name = models.Constraint(
        'unique(name)',
        "Property tag name must be unique.",
    )
