from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)

    _unique_property_tag_name = models.Constraint(
        'UNIQUE(name)',
        'Property tag name must be unique.',
    )
