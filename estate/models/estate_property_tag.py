from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    # SQL Constraints
    # Property tag must be unique
    _unique_property_tag = models.Constraint(
        'UNIQUE(name)',
        'The property tag must be unique',
    )

    name = fields.Char(required=True)
