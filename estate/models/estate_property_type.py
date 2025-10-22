from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    _name_uniq = models.Constraint(
        'unique (name)',
        "A property type name must be unique.",
    )

    name = fields.Char(required=True)
