from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'Property Tag must be unique'),
    ]
