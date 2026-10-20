# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate property type"

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'The type name must be unique.',
    )

    name = fields.Char('Type name', required=True)
