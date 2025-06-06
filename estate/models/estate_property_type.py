from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'Property Type must be unique'),
    ]
