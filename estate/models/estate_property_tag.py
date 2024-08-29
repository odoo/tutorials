from odoo import fields, models


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This module introduces property tags to the real estate model, allowing properties to be categorized with multiple descriptive tags like 'cozy' or 'renovated' using a many-to-many relationship."
    _order = "name"
    _sql_constraints = [
        ('check_tag', 'UNIQUE(name)',
         'A property tag name must be unique'
        ),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

