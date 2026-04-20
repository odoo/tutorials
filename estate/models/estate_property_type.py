from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    name = fields.Char(required=True)

    _unique_type = models.Constraint(
        'unique(name)',
        'Property type should be unique'

    )
