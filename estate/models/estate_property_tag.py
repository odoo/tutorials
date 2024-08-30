from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "property tag model"

    name = fields.Char(required=True)

    _sql_constraints = [('unique_property_tag_name', 'UNIQUE(name)', 'A property tag name must be unique'),
    ]
    