from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        'unique(name)',
        'The type must be unique',
    )
