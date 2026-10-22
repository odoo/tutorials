# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _explanation = "Defines a real estate property type"
    _order = "name"

    name = fields.Char('Property Type', required=True)

    _check_unique = models.Constraint(
        'UNIQUE(name)',
        'A property type with that name already exists.',
    )
